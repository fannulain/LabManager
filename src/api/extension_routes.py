"""
Extension Request REST Controller.
Endpoints:
  POST  /classes/{classId}/materials/{materialId}/extension-requests
  GET   /classes/{classId}/extension-requests
  PATCH /classes/{classId}/extension-requests/{requestId}/decision
"""

from flask import Blueprint, request, jsonify, g
from src.core.security import token_required, class_role_required
from src.services.extension_service import ExtensionService

extension_bp = Blueprint("extensions", __name__)
extension_service = ExtensionService()

@extension_bp.route("/classes/<class_id>/materials/<material_id>/extension-requests", methods=["POST"])
@token_required
@class_role_required(["student", "administrator"])
def submit_extension(class_id, material_id):
    data = request.get_json(silent=True) or {}
    result = extension_service.submit_request(
        class_id=class_id,
        material_id=material_id,
        requester_id=g.current_user_id,
        comment=data.get("comment"),
        requested_deadline=data.get("requested_deadline")
    )
    return jsonify(result), 201

@extension_bp.route("/classes/<class_id>/extension-requests", methods=["GET"])
@token_required
@class_role_required(["administrator", "student"])
def list_extensions(class_id):
    result = extension_service.list_requests(class_id)
    return jsonify(result), 200

@extension_bp.route("/classes/<class_id>/extension-requests/<request_id>/decision", methods=["PATCH"])
@token_required
@class_role_required(["administrator"])
def decide_extension(class_id, request_id):
    data = request.get_json(silent=True) or {}
    result = extension_service.decide_request(
        class_id=class_id,
        request_id=request_id,
        status=data.get("status"),
        resolution_comment=data.get("resolution_comment", ""),
        scope=data.get("scope", "user"),
        acting_user_id=g.current_user_id
    )
    return jsonify(result), 200
