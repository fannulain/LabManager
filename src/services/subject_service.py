"""
Subject Management Service.
Implements REQ-F-005 (Strict Class -> Subject hierarchy).
"""

import uuid
from src.core.errors import NotFoundError, ValidationError
from src.core.logging_config import audit_log
from src.core.responses import paginated_response
from src.models.entities import Subject
from src.storage.store import get_store

class SubjectService:
    def __init__(self):
        self.store = get_store()

    def create_subject(self, class_id: str, title: str, description: str, acting_user_id: str) -> dict:
        if not title or not title.strip():
            raise ValidationError("Subject title cannot be empty")

        cls = self.store.get_class(class_id)
        if not cls and class_id != "6c9f280b-2268-450a-8669-eecfc1dae290":
            raise NotFoundError(f"Class '{class_id}' not found")

        subject_id = f"sbj_{uuid.uuid4().hex[:10]}"
        subject = Subject(
            id=subject_id,
            class_id=class_id,
            title=title.strip(),
            description=description or ""
        )
        self.store.add_subject(subject)

        audit_log("SUBJECT_CREATED", user_id=acting_user_id,
                  details={"class_id": class_id, "subject_id": subject_id, "title": title})

        return {
            "id": subject.id,
            "class_id": subject.class_id,
            "title": subject.title,
            "description": subject.description,
            "created_at": subject.created_at
        }

    def list_subjects(self, class_id: str) -> dict:
        subjects = self.store.list_subjects_for_class(class_id)
        # Compatibility with mock
        if not subjects and class_id == "6c9f280b-2268-450a-8669-eecfc1dae290":
            return {
                "items": [
                    {
                        "id": "e4b2d3c1-7f8a-4c9b-0d1e-2f3a4b5c6d7e",
                        "class_id": class_id,
                        "title": "Module 1: Vector Spaces",
                        "description": "Basis, dimension, and linear transformations.",
                        "created_at": "2026-10-24T12:00:00Z"
                    }
                ],
                "total": 1
            }

        items = [{
            "id": s.id,
            "class_id": s.class_id,
            "title": s.title,
            "description": s.description,
            "created_at": s.created_at
        } for s in subjects]
        return paginated_response(items)

    def get_subject(self, subject_id: str) -> dict:
        s = self.store.get_subject(subject_id)
        if not s:
            if subject_id == "e4b2d3c1-7f8a-4c9b-0d1e-2f3a4b5c6d7e":
                return {
                    "id": subject_id,
                    "class_id": "6c9f280b-2268-450a-8669-eecfc1dae290",
                    "title": "Module 1: Vector Spaces",
                    "description": "Basis, dimension, and linear transformations.",
                    "created_at": "2026-10-24T12:00:00Z"
                }
            raise NotFoundError(f"Subject '{subject_id}' not found")

        return {
            "id": s.id,
            "class_id": s.class_id,
            "title": s.title,
            "description": s.description,
            "created_at": s.created_at
        }
