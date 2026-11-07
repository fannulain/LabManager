"""
Invite REST Controller.
Endpoints:
  POST /classes/{classId}/invites
  POST /invites/{token}/join
"""

from flask import Blueprint, request, jsonify, g
from src.core.security import token_required, class_role_required
from src.services.invite_service import InviteService

invite_bp = Blueprint("invites", __name__)
invite_service = InviteService()

@invite_bp.route("/classes/<class_id>/invites", methods=["POST"])
@token_required
@class_role_required(["administrator"])
def generate_invite(class_id):
    data = request.get_json(silent=True) or {}
    result = invite_service.generate_invite(
        class_id=class_id,
        expires_in_hours=data.get("expires_in_hours", 168),
        max_uses=data.get("max_uses", 100),
        acting_user_id=g.current_user_id
    )
    return jsonify(result), 201

@invite_bp.route("/invites/<token>/join", methods=["POST"])
@token_required
def join_class(token):
    result = invite_service.join_by_invite(
        token=token,
        user_id=g.current_user_id
    )
    return jsonify(result), 200
