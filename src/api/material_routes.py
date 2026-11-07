"""
Material REST Controller.
Endpoints:
  POST /classes/{classId}/subjects/{subjectId}/materials
  GET  /classes/{classId}/subjects/{subjectId}/materials
  GET  /classes/{classId}/subjects/{subjectId}/materials/{materialId}
  GET  /classes/{classId}/subjects/{subjectId}/materials/{materialId}/download
  PUT  /classes/{classId}/subjects/{subjectId}/materials/{materialId}/deadline
"""

from flask import Blueprint, request, jsonify, g, Response
from src.core.security import token_required, class_role_required
from src.services.material_service import MaterialService

material_bp = Blueprint("materials", __name__)
material_service = MaterialService()

@material_bp.route("/classes/<class_id>/subjects/<subject_id>/materials", methods=["POST"])
@token_required
@class_role_required(["administrator"])
def create_material(class_id, subject_id):
    data = request.get_json(silent=True) or {}
    result = material_service.create_material(
        class_id=class_id,
        subject_id=subject_id,
        data=data,
        acting_user_id=g.current_user_id
    )
    return jsonify(result), 201

@material_bp.route("/classes/<class_id>/subjects/<subject_id>/materials", methods=["GET"])
@token_required
@class_role_required(["administrator", "student"])
def list_materials(class_id, subject_id):
    result = material_service.list_materials(class_id, subject_id)
    return jsonify(result), 200

@material_bp.route("/classes/<class_id>/subjects/<subject_id>/materials/<material_id>", methods=["GET"])
@token_required
@class_role_required(["administrator", "student"])
def get_material(class_id, subject_id, material_id):
    result = material_service.get_material(class_id, subject_id, material_id)
    return jsonify(result), 200

@material_bp.route("/classes/<class_id>/subjects/<subject_id>/materials/<material_id>", methods=["DELETE"])
@token_required
@class_role_required(["administrator"])
def delete_material(class_id, subject_id, material_id):
    material_service.delete_material(
        class_id=class_id,
        subject_id=subject_id,
        material_id=material_id,
        acting_user_id=g.current_user_id
    )
    return "", 204

@material_bp.route("/classes/<class_id>/subjects/<subject_id>/materials/<material_id>/download", methods=["GET"])
@token_required
@class_role_required(["administrator", "student"])
def download_material(class_id, subject_id, material_id):
    m = material_service.get_material(class_id, subject_id, material_id)
    content = f"Mock file binary content for material {m['title']}".encode("utf-8")
    return Response(
        content,
        mimetype="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={m['file_name'] or 'material.bin'}"}
    )

@material_bp.route("/classes/<class_id>/subjects/<subject_id>/materials/<material_id>/deadline", methods=["PUT"])
@token_required
@class_role_required(["administrator"])
def update_deadline(class_id, subject_id, material_id):
    data = request.get_json(silent=True) or {}
    result = material_service.update_deadline(
        class_id=class_id,
        subject_id=subject_id,
        material_id=material_id,
        deadline=data.get("deadline"),
        acting_user_id=g.current_user_id
    )
    return jsonify(result), 200
