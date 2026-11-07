"""
In-Memory Storage Component for LabManager.
Provides isolated state repository for entities and relationships.
"""

from typing import Optional
from src.models.entities import (
    User, ClassEntity, ClassMembership, Invite,
    Subject, Material, ExtensionRequest, Reminder
)

class DataStore:
    def __init__(self):
        self.reset()

    def reset(self):
        self.users: dict[str, User] = {}
        self.users_by_email: dict[str, str] = {}
        self.classes: dict[str, ClassEntity] = {}
        self.memberships: dict[str, ClassMembership] = {} # id -> membership
        self.invites: dict[str, Invite] = {} # token -> invite
        self.subjects: dict[str, Subject] = {}
        self.materials: dict[str, Material] = {}
        self.extension_requests: dict[str, ExtensionRequest] = {}
        self.reminders: dict[str, Reminder] = {}

    # User operations
    def add_user(self, user: User):
        self.users[user.id] = user
        self.users_by_email[user.email.lower()] = user.id

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        uid = self.users_by_email.get(email.lower())
        return self.users.get(uid) if uid else None

    # Class operations
    def add_class(self, cls: ClassEntity):
        self.classes[cls.id] = cls

    def get_class(self, class_id: str) -> Optional[ClassEntity]:
        return self.classes.get(class_id)

    # Membership operations
    def add_membership(self, m: ClassMembership):
        self.memberships[m.id] = m

    def get_membership(self, class_id: str, user_id: str) -> Optional[ClassMembership]:
        for m in self.memberships.values():
            if m.class_id == class_id and m.user_id == user_id:
                return m
        return None

    def list_members_for_class(self, class_id: str) -> list[ClassMembership]:
        return [m for m in self.memberships.values() if m.class_id == class_id]

    def list_memberships_for_user(self, user_id: str) -> list[ClassMembership]:
        return [m for m in self.memberships.values() if m.user_id == user_id]

    # Invite operations
    def add_invite(self, invite: Invite):
        self.invites[invite.token] = invite

    def get_invite_by_token(self, token: str) -> Optional[Invite]:
        return self.invites.get(token)

    # Subject operations
    def add_subject(self, subject: Subject):
        self.subjects[subject.id] = subject

    def get_subject(self, subject_id: str) -> Optional[Subject]:
        return self.subjects.get(subject_id)

    def list_subjects_for_class(self, class_id: str) -> list[Subject]:
        return [s for s in self.subjects.values() if s.class_id == class_id]

    # Material operations
    def add_material(self, material: Material):
        self.materials[material.id] = material

    def get_material(self, material_id: str) -> Optional[Material]:
        return self.materials.get(material_id)

    def list_materials_for_subject(self, subject_id: str) -> list[Material]:
        return [m for m in self.materials.values() if m.subject_id == subject_id]

    def list_materials_for_class(self, class_id: str) -> list[Material]:
        return [m for m in self.materials.values() if m.class_id == class_id]

    def delete_material(self, material_id: str) -> bool:
        """Permanently delete material and cascade cleanup to extensions and reminders."""
        if material_id in self.materials:
            del self.materials[material_id]
            # Cascade: remove extension requests for this material
            self.extension_requests = {
                k: v for k, v in self.extension_requests.items() if v.material_id != material_id
            }
            # Cascade: remove reminders for this material
            self.reminders = {
                k: v for k, v in self.reminders.items() if v.material_id != material_id
            }
            return True
        return False

    # Extension Request operations
    def add_extension_request(self, ext: ExtensionRequest):
        self.extension_requests[ext.id] = ext

    def get_extension_request(self, req_id: str) -> Optional[ExtensionRequest]:
        return self.extension_requests.get(req_id)

    def list_extension_requests_for_class(self, class_id: str) -> list[ExtensionRequest]:
        return [r for r in self.extension_requests.values() if r.class_id == class_id]

    # Reminder operations
    def add_reminder(self, reminder: Reminder):
        self.reminders[reminder.id] = reminder

    def get_reminder(self, reminder_id: str) -> Optional[Reminder]:
        return self.reminders.get(reminder_id)

    def list_reminders_for_user(self, user_id: str) -> list[Reminder]:
        return [r for r in self.reminders.values() if r.user_id == user_id]

_GLOBAL_STORE = DataStore()

def get_store() -> DataStore:
    return _GLOBAL_STORE
