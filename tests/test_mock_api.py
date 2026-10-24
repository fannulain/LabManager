"""
Automated Verification Suite for LabManager OpenAPI Mock API.
Executes and validates all Positive (POS) and Negative (NEG) Scenarios
against the OpenAPI Contract and RFC 7807 Problem Details model.
"""

import os
import sys
import pytest

# Ensure scripts dir is on sys.path to import mock_server
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from mock_server import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

AUTH_HEADERS = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.dummy_token"
}

# ==========================================
# POSITIVE SCENARIOS (POS-001 to POS-014)
# ==========================================

def test_pos_001_register_user(client):
    """REQ-F-001: Unified user account registration."""
    res = client.post("/api/v1/auth/register", json={
        "email": "alex.doe@university.edu",
        "password": "SecureP@ssw0rd!",
        "full_name": "Alex Doe"
    })
    assert res.status_code == 201
    data = res.get_json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"
    assert data["user"]["email"] == "alex.doe@university.edu"

def test_pos_002_login_user(client):
    """REQ-F-001: User authentication and JWT issuance."""
    res = client.post("/api/v1/auth/login", json={
        "email": "alex.doe@university.edu",
        "password": "SecureP@ssw0rd!"
    })
    assert res.status_code == 200
    data = res.get_json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"

def test_pos_003_get_current_user_profile(client):
    """REQ-F-001 & REQ-NF-002: Profile retrieval with contextual role distinction."""
    res = client.get("/api/v1/auth/me", headers=AUTH_HEADERS)
    assert res.status_code == 200
    data = res.get_json()
    assert "id" in data
    assert "memberships" in data
    for membership in data["memberships"]:
        assert membership["role"] in ["administrator", "student"]

def test_pos_004_create_class(client):
    """REQ-F-002: Create class container, creator becomes Administrator."""
    res = client.post("/api/v1/classes", headers=AUTH_HEADERS, json={
        "title": "Math 101: Linear Algebra",
        "description": "Linear systems, vector spaces, and eigenvalues."
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data["title"] == "Math 101: Linear Algebra"
    assert data["current_user_role"] == "administrator"

def test_pos_005_list_classes(client):
    """REQ-F-002 & REQ-NF-002: List classes with role distinction."""
    res = client.get("/api/v1/classes", headers=AUTH_HEADERS)
    assert res.status_code == 200
    data = res.get_json()
    assert "items" in data
    assert len(data["items"]) >= 1
    assert data["items"][0]["current_user_role"] in ["administrator", "student"]

def test_pos_006_generate_invite(client):
    """REQ-F-003 & BDD Scenario 1: Administrator generates invite token."""
    res = client.post("/api/v1/classes/6c9f280b-2268-450a-8669-eecfc1dae290/invites", headers=AUTH_HEADERS, json={
        "expires_in_hours": 168
    })
    assert res.status_code == 201
    data = res.get_json()
    assert "invite_token" in data
    assert "invite_url" in data

def test_pos_007_join_class_by_invite(client):
    """REQ-F-003 & BDD Scenario 1: User joins class as Student via token."""
    res = client.post("/api/v1/invites/inv_math101_abc123/join", headers=AUTH_HEADERS)
    assert res.status_code == 200
    data = res.get_json()
    assert data["role"] == "student"

def test_pos_008_promote_member_to_admin(client):
    """REQ-F-004: Administrator grants admin role to another user."""
    res = client.patch(
        "/api/v1/classes/6c9f280b-2268-450a-8669-eecfc1dae290/members/c79b90c2-5509-42b7-a36c-9226cbff207b/role",
        headers=AUTH_HEADERS,
        json={"role": "administrator"}
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["role"] == "administrator"

def test_pos_009_create_subject(client):
    """REQ-F-005: Create academic subject under class (Class -> Subject)."""
    res = client.post(
        "/api/v1/classes/6c9f280b-2268-450a-8669-eecfc1dae290/subjects",
        headers=AUTH_HEADERS,
        json={"title": "Module 1: Matrices and Determinants"}
    )
    assert res.status_code == 201
    data = res.get_json()
    assert data["title"] == "Module 1: Matrices and Determinants"

def test_pos_010_upload_material_file(client):
    """REQ-F-006 & REQ-NF-001: Upload material within 500MB limit."""
    res = client.post(
        "/api/v1/classes/6c9f280b-2268-450a-8669-eecfc1dae290/subjects/495be23b-01a5-484d-a94f-4054a8677c7d/materials",
        headers={**AUTH_HEADERS, "X-Simulate-File-Size": "4194304"}, # 4MB
        json={"title": "Lab 1 Assignment Specification"}
    )
    assert res.status_code == 201
    data = res.get_json()
    assert data["title"] == "Lab 1 Assignment Specification"
    assert data["file_size_bytes"] <= 524288000

def test_pos_011_get_class_calendar(client):
    """REQ-F-007: Built-in calendar deadline tracking."""
    res = client.get(
        "/api/v1/classes/6c9f280b-2268-450a-8669-eecfc1dae290/calendar?from=2026-11-01&to=2026-11-30",
        headers=AUTH_HEADERS
    )
    assert res.status_code == 200
    data = res.get_json()
    assert "items" in data
    assert len(data["items"]) >= 1
    assert "deadline" in data["items"][0]

def test_pos_012_get_reminders(client):
    """REQ-F-008: Internal reminders (7-day and 1-day triggers)."""
    res = client.get("/api/v1/reminders", headers=AUTH_HEADERS)
    assert res.status_code == 200
    data = res.get_json()
    assert "items" in data
    assert data["items"][0]["trigger_type"] in ["7_day", "1_day"]

def test_pos_013_submit_extension_request(client):
    """REQ-F-009 & BDD Scenario 2: Student submits extension request with comment."""
    res = client.post(
        "/api/v1/classes/6c9f280b-2268-450a-8669-eecfc1dae290/materials/991e0a29-2325-4c07-b769-cf76e1919a31/extension-requests",
        headers=AUTH_HEADERS,
        json={
            "comment": "I was sick with flu and couldn't access my dev environment.",
            "requested_deadline": "2026-11-17T23:59:59Z"
        }
    )
    assert res.status_code == 201
    data = res.get_json()
    assert data["status"] == "pending"
    assert "I was sick" in data["comment"]

def test_pos_014_decide_extension_request(client):
    """REQ-F-010: Administrator approves extension request and updates deadline."""
    res = client.patch(
        "/api/v1/classes/6c9f280b-2268-450a-8669-eecfc1dae290/extension-requests/d19c3e98-c114-46f9-bb20-1b7774ad825e/decision",
        headers=AUTH_HEADERS,
        json={
            "decision": "approved",
            "scope": "user",
            "new_deadline": "2026-11-17T23:59:59Z",
            "resolution_comment": "Approved upon medical note."
        }
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] in ["approved", "pending"]


# ==========================================
# NEGATIVE SCENARIOS (NEG-001 to NEG-007)
# ==========================================

def test_neg_001_unauthorized_access(client):
    """NEG-001: Missing Authorization Bearer token returns 401 Problem Details."""
    res = client.get("/api/v1/classes")
    assert res.status_code == 401
    assert res.mimetype == "application/problem+json"
    data = res.get_json()
    assert data["status"] == 401
    assert data["title"] == "Unauthorized"
    assert "type" in data
    assert "detail" in data

def test_neg_002_forbidden_student_action(client):
    """NEG-002: BDD Scenario 1 - Student cannot perform admin actions (403 Forbidden)."""
    res = client.post(
        "/api/v1/classes/6c9f280b-2268-450a-8669-eecfc1dae290/subjects",
        headers={**AUTH_HEADERS, "X-Simulate-Role": "student"},
        json={"title": "Hacked Subject"}
    )
    assert res.status_code == 403
    assert res.mimetype == "application/problem+json"
    data = res.get_json()
    assert data["status"] == 403
    assert data["title"] == "Forbidden"
    assert "Only Class Administrators" in data["detail"]

def test_neg_003_resource_not_found(client):
    """NEG-003: Requesting non-existent route or resource returns 404 Problem Details."""
    res = client.get(
        "/api/v1/classes/non-existent-uuid",
        headers={**AUTH_HEADERS, "X-Mock-Status": "404"}
    )
    assert res.status_code == 404
    assert res.mimetype == "application/problem+json"
    data = res.get_json()
    assert data["status"] == 404
    assert data["title"] == "Not Found"

def test_neg_004_conflict_state(client):
    """NEG-004: Duplicate registration or duplicate class member returns 409 Conflict."""
    res = client.post(
        "/api/v1/auth/register",
        headers={"X-Mock-Status": "409"},
        json={"email": "duplicate@university.edu", "password": "pass", "full_name": "Dup"}
    )
    assert res.status_code == 409
    assert res.mimetype == "application/problem+json"
    data = res.get_json()
    assert data["status"] == 409
    assert data["title"] == "Conflict"

def test_neg_005_oversized_file_upload(client):
    """NEG-005: REQ-NF-001 & BDD Scenario 3 - File > 500MB returns 413 Payload Too Large."""
    # Simulate 600MB file (629,145,600 bytes)
    res = client.post(
        "/api/v1/classes/6c9f280b-2268-450a-8669-eecfc1dae290/subjects/495be23b-01a5-484d-a94f-4054a8677c7d/materials",
        headers={**AUTH_HEADERS, "X-Simulate-File-Size": "629145600"},
        json={"title": "Huge Assignment"}
    )
    assert res.status_code == 413
    assert res.mimetype == "application/problem+json"
    data = res.get_json()
    assert data["status"] == 413
    assert data["title"] == "Payload Too Large"
    assert "File exceeds the 500MB limit" in data["detail"]
    assert "invalid_params" in data
    assert data["invalid_params"][0]["name"] == "file"

def test_neg_006_unprocessable_entity_validation_failure(client):
    """NEG-006: Validation error returns 422 Problem Details with invalid_params."""
    res = client.post(
        "/api/v1/classes",
        headers={**AUTH_HEADERS, "X-Mock-Status": "422"},
        json={"title": "x"} # Invalid short title
    )
    assert res.status_code == 422
    assert res.mimetype == "application/problem+json"
    data = res.get_json()
    assert data["status"] == 422
    assert data["title"] == "Unprocessable Entity"
    assert "invalid_params" in data

def test_neg_007_bad_request_malformed_syntax(client):
    """NEG-007: Malformed syntax returns 400 Bad Request Problem Details."""
    res = client.post(
        "/api/v1/auth/login",
        headers={"X-Mock-Status": "400"},
        data="not a json"
    )
    assert res.status_code == 400
    assert res.mimetype == "application/problem+json"
    data = res.get_json()
    assert data["status"] == 400
    assert data["title"] == "Bad Request"
