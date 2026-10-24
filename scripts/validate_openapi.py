#!/usr/bin/env python3
"""
Automated OpenAPI 3.0.3 Specification Validator.
Validates syntax, structural conformance, internal $ref pointer resolution,
RFC 7807 Problem Details compliance, and SRS requirement coverage.
"""

import json
import os
import sys
import jsonschema

SPEC_PATH = os.path.join(os.path.dirname(__file__), "..", "spec", "openapi.json")

REQUIRED_REQ_IDS = [
    "REQ-F-001",
    "REQ-F-002",
    "REQ-F-003",
    "REQ-F-004",
    "REQ-F-005",
    "REQ-F-006",
    "REQ-F-007",
    "REQ-F-008",
    "REQ-F-009",
    "REQ-F-010",
    "REQ-NF-001",
    "REQ-NF-002",
]

def resolve_pointer(root, pointer: str):
    if not pointer.startswith("#/"):
        raise ValueError(f"External $ref not supported: {pointer}")
    parts = pointer[2:].split("/")
    cur = root
    for p in parts:
        p = p.replace("~1", "/").replace("~0", "~")
        if p not in cur:
            raise KeyError(f"Failed resolving pointer '{pointer}' at segment '{p}'")
        cur = cur[p]
    return cur

def validate_openapi():
    print(f"[*] Loading specification from: {SPEC_PATH}")
    if not os.path.exists(SPEC_PATH):
        print(f"[FAIL] Specification file not found at {SPEC_PATH}")
        return False

    with open(SPEC_PATH, "r", encoding="utf-8") as f:
        try:
            spec = json.load(f)
        except Exception as e:
            print(f"[FAIL] JSON syntax error: {e}")
            return False

    errors = []
    warnings = []

    # 1. Top-level fields
    for field in ["openapi", "info", "paths", "components"]:
        if field not in spec:
            errors.append(f"Missing required top-level field: '{field}'")

    if not spec.get("openapi", "").startswith("3.0"):
        errors.append(f"Invalid OpenAPI version: {spec.get('openapi')}")

    info = spec.get("info", {})
    if not info.get("title") or not info.get("version"):
        errors.append("info object must contain 'title' and 'version'")

    # 2. Validate all $refs recursively
    resolved_refs_count = 0
    def check_refs(node, path=""):
        nonlocal resolved_refs_count
        if isinstance(node, dict):
            if "$ref" in node:
                ref = node["$ref"]
                try:
                    resolve_pointer(spec, ref)
                    resolved_refs_count += 1
                except Exception as ex:
                    errors.append(f"Broken $ref at '{path}': {ref} -> {ex}")
            for k, v in node.items():
                check_refs(v, f"{path}/{k}")
        elif isinstance(node, list):
            for idx, item in enumerate(node):
                check_refs(item, f"{path}[{idx}]")

    check_refs(spec)
    print(f"[*] Verified and resolved {resolved_refs_count} internal $ref references.")

    # 3. Paths & Operations
    paths = spec.get("paths", {})
    operation_ids = set()
    total_operations = 0
    http_methods = {"get", "post", "put", "patch", "delete", "options", "head"}

    for path_key, path_item in paths.items():
        if not path_key.startswith("/"):
            errors.append(f"Path does not start with '/': {path_key}")
        for method, op in path_item.items():
            if method.lower() not in http_methods:
                continue
            total_operations += 1
            op_id = op.get("operationId")
            if not op_id:
                errors.append(f"Operation {method.upper()} {path_key} missing operationId")
            elif op_id in operation_ids:
                errors.append(f"Duplicate operationId: '{op_id}'")
            else:
                operation_ids.add(op_id)

            if not op.get("summary"):
                warnings.append(f"Operation '{op_id}' missing summary")
            if not op.get("tags"):
                warnings.append(f"Operation '{op_id}' missing tags")

            responses = op.get("responses", {})
            if not responses:
                errors.append(f"Operation '{op_id}' has no responses defined")

            # Check success code
            has_success = any(code.startswith("2") for code in responses.keys())
            if not has_success:
                errors.append(f"Operation '{op_id}' has no 2xx success response")

    print(f"[*] Validated {len(paths)} paths and {total_operations} operations.")

    # 4. Schemas validation
    schemas = spec.get("components", {}).get("schemas", {})
    if "ProblemDetails" not in schemas:
        errors.append("RFC 7807 'ProblemDetails' schema missing in components/schemas")

    # Validate each schema structure using jsonschema Draft7Validator
    for s_name, s_body in schemas.items():
        try:
            # Check draft-7 valid schema declaration
            jsonschema.Draft7Validator.check_schema(s_body)
        except Exception as ex:
            errors.append(f"Schema '{s_name}' is not valid JSON Schema: {ex}")

    # 5. Check SRS requirements coverage in spec
    full_spec_text = json.dumps(spec)
    missing_reqs = []
    for req in REQUIRED_REQ_IDS:
        if req not in full_spec_text:
            missing_reqs.append(req)

    if missing_reqs:
        errors.append(f"SRS requirements not traced in OpenAPI specification: {missing_reqs}")
    else:
        print(f"[*] Verified that all {len(REQUIRED_REQ_IDS)} SRS requirements are referenced in the OpenAPI spec.")

    print("\n--- VALIDATION SUMMARY ---")
    if warnings:
        print(f"[!] Warnings ({len(warnings)}):")
        for w in warnings:
            print(f"    - {w}")

    if errors:
        print(f"[FAIL] Errors ({len(errors)}):")
        for err in errors:
            print(f"    - {err}")
        return False

    print("[SUCCESS] OpenAPI specification passed all validation checks successfully!")
    print(f"Total Paths: {len(paths)}")
    print(f"Total Operations: {total_operations}")
    print(f"Total Schemas: {len(schemas)}")
    return True

if __name__ == "__main__":
    success = validate_openapi()
    sys.exit(0 if success else 1)
