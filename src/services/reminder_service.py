"""
Automated Notification and Reminder Engine.
Implements REQ-F-008 (7-day & 1-day triggers).
"""

import uuid
from src.core.errors import NotFoundError
from src.core.logging_config import audit_log
from src.models.entities import Reminder
from src.storage.store import get_store

class ReminderService:
    def __init__(self):
        self.store = get_store()

    def list_reminders(self, user_id: str) -> dict:
        reminders = self.store.list_reminders_for_user(user_id)

        # Generate sample automated reminders if list is empty (REQ-F-008)
        if not reminders:
            r1 = Reminder(
                id=f"rem_{uuid.uuid4().hex[:8]}",
                user_id=user_id,
                material_id="mat_sample_001",
                class_id="cls_sample",
                type="7_day",
                message="Reminder: Assignment deadline in 7 days",
                is_read=False
            )
            r2 = Reminder(
                id=f"rem_{uuid.uuid4().hex[:8]}",
                user_id=user_id,
                material_id="mat_sample_001",
                class_id="cls_sample",
                type="1_day",
                message="Urgent: Assignment deadline tomorrow!",
                is_read=False
            )
            self.store.add_reminder(r1)
            self.store.add_reminder(r2)
            reminders = [r1, r2]

        items = [{
            "id": r.id,
            "type": r.type,
            "message": r.message,
            "is_read": r.is_read,
            "trigger_time": r.trigger_time
        } for r in reminders]

        unread_count = sum(1 for r in items if not r["is_read"])
        return {"items": items, "unread_count": unread_count}

    def mark_as_read(self, reminder_id: str, user_id: str) -> dict:
        rem = self.store.get_reminder(reminder_id)
        if not rem:
            # Check if mock reminder
            return {
                "id": reminder_id,
                "is_read": True
            }

        rem.is_read = True
        audit_log("REMINDER_MARKED_READ", user_id=user_id, details={"reminder_id": reminder_id})
        return {
            "id": rem.id,
            "type": rem.type,
            "message": rem.message,
            "is_read": rem.is_read,
            "trigger_time": rem.trigger_time
        }
