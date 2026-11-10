"""
LabManager REST API Application Factory.
Configures component blueprints, RFC 7807 error handling, and structured request logging.
"""

import os
import sys

# Ensure project root is present in sys.path when running as `python src/app.py`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, request, g, render_template, jsonify, send_file
from src.core.errors import register_error_handlers
from src.core.logging_config import setup_logging, audit_log, logger
from src.api.auth_routes import auth_bp
from src.api.class_routes import class_bp
from src.api.invite_routes import invite_bp
from src.api.subject_routes import subject_bp
from src.api.material_routes import material_bp
from src.api.calendar_routes import calendar_bp
from src.api.reminder_routes import reminder_bp
from src.api.extension_routes import extension_bp

def create_app(config: dict = None) -> Flask:
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    if config:
        app.config.update(config)

    # Initialize logging
    log_file = app.config.get("LOG_FILE")
    setup_logging(log_file)

    # Register RFC 7807 problem details handlers
    register_error_handlers(app)

    # Register blueprints under /api/v1
    prefix = "/api/v1"
    app.register_blueprint(auth_bp, url_prefix=prefix)
    app.register_blueprint(class_bp, url_prefix=prefix)
    app.register_blueprint(invite_bp, url_prefix=prefix)
    app.register_blueprint(subject_bp, url_prefix=prefix)
    app.register_blueprint(material_bp, url_prefix=prefix)
    app.register_blueprint(calendar_bp, url_prefix=prefix)
    app.register_blueprint(reminder_bp, url_prefix=prefix)
    app.register_blueprint(extension_bp, url_prefix=prefix)

    # Web UI Dashboard & Documentation routes
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/api/v1/system/logs", methods=["GET"])
    def get_system_logs():
        log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs", "system.log"))
        lines = []
        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()[-60:]
        return jsonify({"lines": [line.strip() for line in lines if line.strip()]}), 200

    @app.route("/api/v1/spec", methods=["GET"])
    def get_openapi_spec():
        spec_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "spec", "openapi.json"))
        if os.path.exists(spec_path):
            return send_file(spec_path, mimetype="application/json")
        return jsonify({"error": "Specification file not found"}), 404

    @app.before_request
    def log_incoming_request():
        audit_log("REQUEST_RECEIVED",
                  user_id=getattr(g, "current_user_id", None),
                  details={"method": request.method, "path": request.path, "ip": request.remote_addr},
                  level="DEBUG")

    @app.after_request
    def log_response_completion(response):
        audit_log("REQUEST_COMPLETED",
                  user_id=getattr(g, "current_user_id", None),
                  details={"method": request.method, "path": request.path, "status": response.status_code},
                  level="DEBUG")
        return response

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)
