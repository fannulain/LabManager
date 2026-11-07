"""
Calendar REST Controller.
Endpoints:
  GET /classes/{classId}/calendar
  GET /calendar
"""

from flask import Blueprint, request, jsonify, g
from src.core.security import token_required, class_role_required
from src.services.calendar_service import CalendarService

calendar_bp = Blueprint("calendar", __name__)
calendar_service = CalendarService()

@calendar_bp.route("/classes/<class_id>/calendar", methods=["GET"])
@token_required
@class_role_required(["administrator", "student"])
def get_class_calendar(class_id):
    from_date = request.args.get("from")
    to_date = request.args.get("to")
    result = calendar_service.get_class_calendar(class_id, from_date, to_date)
    return jsonify(result), 200

@calendar_bp.route("/calendar", methods=["GET"])
@token_required
def get_global_calendar():
    from_date = request.args.get("from")
    to_date = request.args.get("to")
    result = calendar_service.get_global_calendar(g.current_user_id, from_date, to_date)
    return jsonify(result), 200
