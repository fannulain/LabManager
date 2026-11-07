"""
Auth REST Controller.
Endpoints: /auth/register, /auth/login, /auth/me
"""

from flask import Blueprint, request, jsonify, g
from src.core.security import token_required
from src.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__)
auth_service = AuthService()

@auth_bp.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    result = auth_service.register(
        email=data.get("email"),
        password=data.get("password"),
        full_name=data.get("full_name", "")
    )
    return jsonify(result), 201

@auth_bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    result = auth_service.login(
        email=data.get("email"),
        password=data.get("password")
    )
    return jsonify(result), 200

@auth_bp.route("/auth/me", methods=["GET"])
@token_required
def get_current_user():
    result = auth_service.get_profile(g.current_user_id)
    return jsonify(result), 200
