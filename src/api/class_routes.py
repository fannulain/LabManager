"""
Class and Membership REST Controller.
Endpoints:
  POST /classes
  GET  /classes
  GET  /classes/{classId}
  GET  /classes/{classId}/members
  PATCH /classes/{classId}/members/{userId}/role
"""

from flask import Blueprint, request, jsonify, g
from src.core.security import token_required, class_role_required
from src.services.class_service import ClassService

class_bp = Blueprint("classes", __name__)
class_service = ClassService()

@class_bp.route("/classes", methods=["POST"])
@token_required
def create_class():
    data = request.get_json(silent=True) or {}
    result = class_service.create_class(
        title=data.get("title"),
        description=data.get("description", ""),
        owner_id=g.current_user_id
    )
    return jsonify(result), 201

@class_bp.route("/classes", methods=["GET"])
@token_required
def list_classes():
    result = class_service.list_classes(g.current_user_id)
    return jsonify(result), 200

@class_bp.route("/classes/<class_id>", methods=["GET"])
@token_required
def get_class(class_id):
    result = class_service.get_class(class_id, g.current_user_id)
    return jsonify(result), 200

@class_bp.route("/classes/<class_id>/members", methods=["GET"])
@token_required
def list_members(class_id):
    result = class_service.list_members(class_id)
    return jsonify(result), 200

@class_bp.route("/classes/<class_id>/members/<user_id>/role", methods=["PATCH"])
@token_required
@class_role_required(["administrator"])
def update_member_role(class_id, user_id):
    data = request.get_json(silent=True) or {}
    result = class_service.update_member_role(
        class_id=class_id,
        target_user_id=user_id,
        new_role=data.get("role"),
        acting_user_id=g.current_user_id
    )
    return jsonify(result), 200
