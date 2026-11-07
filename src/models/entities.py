"""
Domain Entities and Data Classes for LabManager.
Aligned with OpenAPI Schemas and SRS Domain Glossary.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import uuid

def current_utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class User:
    id: str
    email: str
    password_hash: str
    salt: str
    full_name: str
    created_at: str = field(default_factory=current_utc_iso)

@dataclass
class ClassEntity:
    id: str
    title: str
    description: str
    owner_id: str
    created_at: str = field(default_factory=current_utc_iso)

@dataclass
class ClassMembership:
    id: str
    class_id: str
    user_id: str
    role: str  # 'administrator' | 'student'
    joined_at: str = field(default_factory=current_utc_iso)

@dataclass
class Invite:
    id: str
    class_id: str
    token: str
    expires_at: str
    max_uses: int = 100
    uses_count: int = 0
    created_at: str = field(default_factory=current_utc_iso)

@dataclass
class Subject:
    id: str
    class_id: str
    title: str
    description: str
    created_at: str = field(default_factory=current_utc_iso)

@dataclass
class Material:
    id: str
    subject_id: str
    class_id: str
    title: str
    description: str
    type: str  # 'file' | 'link'
    file_name: str = ""
    file_url: str = ""
    file_size_bytes: int = 0
    link_url: str = ""
    deadline: str = None
    created_at: str = field(default_factory=current_utc_iso)

@dataclass
class ExtensionRequest:
    id: str
    class_id: str
    material_id: str
    requester_id: str
    comment: str
    requested_deadline: str
    status: str = "pending"  # 'pending' | 'approved' | 'rejected'
    resolution_comment: str = ""
    scope: str = "user"  # 'user' | 'class'
    created_at: str = field(default_factory=current_utc_iso)
    resolved_at: str = None

@dataclass
class Reminder:
    id: str
    user_id: str
    material_id: str
    class_id: str
    type: str  # '7_day' | '1_day'
    message: str
    is_read: bool = False
    trigger_time: str = field(default_factory=current_utc_iso)
    created_at: str = field(default_factory=current_utc_iso)
