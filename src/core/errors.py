"""
RFC 7807 (RFC 9457) Problem Details Error Handling Component.
Ensures uniform REST error payloads and status codes across the entire API.
"""

from flask import jsonify, request
from werkzeug.exceptions import HTTPException
from src.core.logging_config import logger, audit_log

class ApiError(Exception):
    def __init__(self, status_code: int, title: str, detail: str,
                 type_uri: str = None, invalid_params: list = None):
        super().__init__(detail)
        self.status_code = status_code
        self.title = title
        self.detail = detail
        self.type_uri = type_uri or f"https://labmanager.edu/errors/{title.lower().replace(' ', '-')}"
        self.invalid_params = invalid_params or []

    def to_dict(self):
        data = {
            "type": self.type_uri,
            "title": self.title,
            "status": self.status_code,
            "detail": self.detail,
            "instance": request.path if request else "/"
        }
        if self.invalid_params:
            data["invalid_params"] = self.invalid_params
        return data

class BadRequestError(ApiError):
    def __init__(self, detail: str = "Invalid request syntax or body", invalid_params: list = None):
        super().__init__(400, "Bad Request", detail, invalid_params=invalid_params)

class UnauthorizedError(ApiError):
    def __init__(self, detail: str = "Authentication token missing or invalid"):
        super().__init__(401, "Unauthorized", detail,
                         type_uri="https://labmanager.edu/errors/unauthorized")

class ForbiddenError(ApiError):
    def __init__(self, detail: str = "Access forbidden: insufficient permissions"):
        super().__init__(403, "Forbidden", detail,
                         type_uri="https://labmanager.edu/errors/forbidden")

class NotFoundError(ApiError):
    def __init__(self, detail: str = "Requested resource not found"):
        super().__init__(404, "Not Found", detail,
                         type_uri="https://labmanager.edu/errors/not-found")

class ConflictError(ApiError):
    def __init__(self, detail: str = "Resource state conflict"):
        super().__init__(409, "Conflict", detail,
                         type_uri="https://labmanager.edu/errors/conflict")

class PayloadTooLargeError(ApiError):
    def __init__(self, detail: str = "File exceeds the 500MB limit. Maximum allowed size is 524288000 bytes.", invalid_params: list = None):
        super().__init__(413, "Payload Too Large", detail,
                         type_uri="https://labmanager.edu/errors/file-too-large",
                         invalid_params=invalid_params)

class ValidationError(ApiError):
    def __init__(self, detail: str = "Semantic validation failed", invalid_params: list = None):
        super().__init__(422, "Unprocessable Entity", detail,
                         type_uri="https://labmanager.edu/errors/validation-failed",
                         invalid_params=invalid_params)

def register_error_handlers(app):
    """Register uniform RFC 7807 error handlers on Flask application."""

    @app.errorhandler(ApiError)
    def handle_api_error(err):
        audit_log("API_ERROR_RETURNED", details={"status": err.status_code, "title": err.title, "detail": err.detail, "path": request.path}, level="WARNING")
        response = jsonify(err.to_dict())
        response.status_code = err.status_code
        response.headers["Content-Type"] = "application/problem+json"
        return response

    @app.errorhandler(HTTPException)
    def handle_http_exception(err):
        audit_log("HTTP_EXCEPTION_CAUGHT", details={"status": err.code, "description": err.description, "path": request.path}, level="WARNING")
        payload = {
            "type": f"https://labmanager.edu/errors/{err.name.lower().replace(' ', '-')}",
            "title": err.name,
            "status": err.code,
            "detail": err.description,
            "instance": request.path
        }
        response = jsonify(payload)
        response.status_code = err.code
        response.headers["Content-Type"] = "application/problem+json"
        return response

    @app.errorhandler(Exception)
    def handle_unexpected_exception(err):
        logger.exception("Unexpected server error: %s", err)
        audit_log("INTERNAL_SERVER_ERROR", details={"error": str(err), "path": request.path}, level="ERROR")
        payload = {
            "type": "https://labmanager.edu/errors/internal-server-error",
            "title": "Internal Server Error",
            "status": 500,
            "detail": "An unexpected error occurred processing your request.",
            "instance": request.path
        }
        response = jsonify(payload)
        response.status_code = 500
        response.headers["Content-Type"] = "application/problem+json"
        return response
