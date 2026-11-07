"""
Subject REST Controller.
Endpoints:
  POST /classes/{classId}/subjects
  GET  /classes/{classId}/subjects
  GET  /classes/{classId}/subjects/{subjectId}
"""

from flask import Blueprint, request, jsonify, g
from src.core.security import token_required, class_role_required
from src.services.subject_service import SubjectService

subject_bp = Blueprint("subjects", __name__)
subject_service = SubjectService()

@subject_bp.route("/classes/<class_id>/subjects", methods=["POST"])
@token_required
@class_role_required(["administrator"])
def create_subject(class_id):
    data = request.get_json(silent=True) or {}
    result = subject_service.create_subject(
        class_id=class_id,
        title=data.get("title"),
        description=data.get("description", ""),
        acting_user_id=g.current_user_id
    )
    return jsonify(result), 201

@subject_bp.route("/classes/<class_id>/subjects", methods=["GET"])
@token_required
@class_role_required(["administrator", "student"])
def list_subjects(class_id):
    result = subject_service.list_subjects(class_id)
    return jsonify(result), 200

@subject_bp.route("/classes/<class_id>/subjects/<subject_id>", methods=["GET"])
@token_required
@class_role_required(["administrator", "student"])
def get_subject(class_id, subject_id):
    result = subject_service.get_subject(subject_id)
    return jsonify(result), 200
