#!/usr/bin/env python3
"""
OpenAPI Specification-Driven Mock API Server.
Dynamically serves endpoints defined in spec/openapi.json without implementing server business logic.
Supports positive scenarios (schema/example responses) and negative scenarios (RFC 7807 problem details).
"""

import json
import os
import re
from flask import Flask, request, jsonify, Response

SPEC_PATH = os.path.join(os.path.dirname(__file__), "..", "spec", "openapi.json")

app = Flask(__name__)

def load_spec():
    with open(SPEC_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

SPEC = load_spec()

def resolve_ref(root, ref: str):
    if not ref.startswith("#/"):
        return {}
    parts = ref[2:].split("/")
    cur = root
    for p in parts:
        p = p.replace("~1", "/").replace("~0", "~")
        cur = cur.get(p, {})
    return cur

def match_path(req_path: str):
    # Strip base prefix /api/v1 if present
    path = req_path
    if path.startswith("/api/v1"):
        path = path[len("/api/v1"):]
    if not path:
        path = "/"

    for spec_path, path_item in SPEC.get("paths", {}).items():
        # Convert {param} to regex pattern
        pattern = re.sub(r"\{[a-zA-Z0-9_]+\}", r"([^/]+)", spec_path)
        pattern = f"^{pattern}$"
        match = re.match(pattern, path)
        if match:
            return spec_path, path_item, match.groups()
    return None, None, None

def get_example_from_response(resp_obj):
    # Direct example on content
    content = resp_obj.get("content", {})
    for c_type in ["application/json", "application/problem+json", "*/*"]:
        if c_type in content:
            c_val = content[c_type]
            if "example" in c_val:
                return c_val["example"], c_type
            if "schema" in c_val:
                schema = c_val["schema"]
                if "$ref" in schema:
                    schema = resolve_ref(SPEC, schema["$ref"])
                if "example" in schema:
                    return schema["example"], c_type
                # Synthesize from schema properties
                return synthesize_from_schema(schema), c_type
    return {}, "application/json"

def synthesize_from_schema(schema):
    if not schema:
        return {}
    if "allOf" in schema:
        merged = {}
        for sub in schema["allOf"]:
            if "$ref" in sub:
                sub = resolve_ref(SPEC, sub["$ref"])
            merged.update(synthesize_from_schema(sub))
        return merged

    s_type = schema.get("type", "object")
    if s_type == "object":
        res = {}
        props = schema.get("properties", {})
        for prop_name, prop_val in props.items():
            if "$ref" in prop_val:
                prop_val = resolve_ref(SPEC, prop_val["$ref"])
            if "example" in prop_val:
                res[prop_name] = prop_val["example"]
            elif prop_val.get("type") == "object" or "properties" in prop_val or "allOf" in prop_val:
                res[prop_name] = synthesize_from_schema(prop_val)
            elif prop_val.get("type") == "array":
                item_schema = prop_val.get("items", {})
                if "$ref" in item_schema:
                    item_schema = resolve_ref(SPEC, item_schema["$ref"])
                res[prop_name] = [synthesize_from_schema(item_schema)]
            elif prop_val.get("type") == "string":
                res[prop_name] = "sample_string"
            elif prop_val.get("type") == "integer":
                res[prop_name] = 1
            elif prop_val.get("type") == "boolean":
                res[prop_name] = True
            else:
                res[prop_name] = None
        return res
    elif s_type == "array":
        item_schema = schema.get("items", {})
        if "$ref" in item_schema:
            item_schema = resolve_ref(SPEC, item_schema["$ref"])
        return [synthesize_from_schema(item_schema)]
    return {}

@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"])
def catch_all(path):
    full_path = "/" + path
    method = request.method.lower()

    # Health check endpoint for mock server
    if full_path in ["/health", "/api/v1/health"]:
        return jsonify({"status": "mock-server-running", "version": SPEC["info"]["version"]}), 200

    spec_path, path_item, _ = match_path(full_path)
    if not path_item or method not in path_item:
        problem = {
            "type": "https://labmanager.edu/errors/not-found",
            "title": "Not Found",
            "status": 404,
            "detail": f"No OpenAPI operation defined for {request.method} {full_path}",
            "instance": full_path
        }
        return Response(json.dumps(problem), status=404, mimetype="application/problem+json")

    operation = path_item[method]
    responses = operation.get("responses", {})

    # Check for client-requested mock code (Prefer: code=XXX or query param ?mock_status=XXX)
    requested_code = request.headers.get("X-Mock-Status") or request.args.get("mock_status")
    prefer = request.headers.get("Prefer", "")
    if "code=" in prefer:
        requested_code = prefer.split("code=")[1].split(",")[0].strip()

    # Rule-based dynamic negative scenario triggers
    # 1. Check file size > 500MB (REQ-NF-001, BDD Scenario 3)
    if "materials" in full_path and method == "post":
        content_length = request.content_length or 0
        file_size_header = request.headers.get("X-Simulate-File-Size")
        if file_size_header and int(file_size_header) > 524288000:
            content_length = int(file_size_header)

        if content_length > 524288000:
            problem = {
                "type": "https://labmanager.edu/errors/file-too-large",
                "title": "Payload Too Large",
                "status": 413,
                "detail": "File exceeds the 500MB limit.",
                "instance": full_path,
                "invalid_params": [
                    {
                        "name": "file",
                        "reason": f"Uploaded file size ({content_length} bytes) exceeds maximum allowable limit of 524288000 bytes."
                    }
                ]
            }
            return Response(json.dumps(problem), status=413, mimetype="application/problem+json")

    # 2. Check missing Bearer token on protected routes
    security = operation.get("security", SPEC.get("security", []))
    if security:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            problem = {
                "type": "https://labmanager.edu/errors/unauthorized",
                "title": "Unauthorized",
                "status": 401,
                "detail": "Missing or invalid Bearer authentication token.",
                "instance": full_path
            }
            return Response(json.dumps(problem), status=401, mimetype="application/problem+json")

    # 3. Simulate forbidden student access on admin operations
    if request.headers.get("X-Simulate-Role") == "student" and (
        "subjects" in full_path and method == "post" or
        "invites" in full_path and method == "post" or
        "role" in full_path and method == "patch" or
        "decision" in full_path and method == "patch" or
        ("materials" in full_path and method == "post")
    ):
        problem = {
            "type": "https://labmanager.edu/errors/forbidden",
            "title": "Forbidden",
            "status": 403,
            "detail": "Only Class Administrators are permitted to perform this action.",
            "instance": full_path
        }
        return Response(json.dumps(problem), status=403, mimetype="application/problem+json")

    # 4. Handle requested status code if specified
    if requested_code and str(requested_code) in responses:
        resp_def = responses[str(requested_code)]
        if "$ref" in resp_def:
            resp_def = resolve_ref(SPEC, resp_def["$ref"])
        data, mime = get_example_from_response(resp_def)
        return Response(json.dumps(data), status=int(requested_code), mimetype=mime)

    # 5. Default success response (200, 201, 204)
    success_codes = [c for c in responses.keys() if c.startswith("2")]
    if success_codes:
        code_str = min(success_codes) # e.g. 200 or 201
        status_code = int(code_str)
        if status_code == 204:
            return Response("", status=204)
        resp_def = responses[code_str]
        if "$ref" in resp_def:
            resp_def = resolve_ref(SPEC, resp_def["$ref"])
        data, mime = get_example_from_response(resp_def)
        resp = Response(json.dumps(data), status=status_code, mimetype=mime)
        resp.headers["X-Mock-Engine"] = "LabManager-OpenAPI-Mock/1.0"
        return resp

    return jsonify({"error": "No mock response configured"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"[*] Starting LabManager Mock API Server on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=False)
