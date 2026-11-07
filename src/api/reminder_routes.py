"""
Reminder REST Controller.
Endpoints:
  GET   /reminders
  PATCH /reminders/{reminderId}/read
"""

from flask import Blueprint, request, jsonify, g
from src.core.security import token_required
from src.services.reminder_service import ReminderService

reminder_bp = Blueprint("reminders", __name__)
reminder_service = ReminderService()

@reminder_bp.route("/reminders", methods=["GET"])
@token_required
def list_reminders():
    result = reminder_service.list_reminders(g.current_user_id)
    return jsonify(result), 200

@reminder_bp.route("/reminders/<reminder_id>/read", methods=["PATCH"])
@token_required
def mark_read(reminder_id):
    result = reminder_service.mark_as_read(reminder_id, g.current_user_id)
    return jsonify(result), 200
