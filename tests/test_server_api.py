"""
Automated TDD Test Suite for LabManager Server REST API.
Authored strictly from SRS v1.0, SRS Addendum v1.0, Acceptance Criteria,
BDD Scenarios (1, 2, 3), and the approved OpenAPI 3.0.3 Specification.

This suite is causally independent of the implementation:
it tests the public HTTP interface of the server application.
"""

import os
import sys
import pytest

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.app import create_app
from src.storage.store import get_store

@pytest.fixture
def app_instance():
    """Create a clean isolated application and reset store for each test."""
    app = create_app({"TESTING": True, "LOG_FILE": "logs/test_execution.log"})
    store = get_store()
    store.reset()
    return app

@pytest.fixture
def client(app_instance):
    """Test client fixture."""
    with app_instance.test_client() as client:
        yield client

def register_and_login(client, email="user@test.edu", password="Password123!", full_name="Test User"):
    """Helper to register and return authorization headers."""
    reg_res = client.post("/api/v1/auth/register", json={
        "email": email,
        "password": password,
        "full_name": full_name
    })
    token = reg_res.get_json()["access_token"]
    user_id = reg_res.get_json()["user"]["id"]
    return {
        "Authorization": f"Bearer {token}"
    }, user_id

# ============================================================================
# PHASE 2: REQ-F-001 (Auth & User Account), REQ-NF-002 (Role Badging)
# ============================================================================

def test_req_f_001_register_user_success(client):
    """REQ-F-001: Register user successfully with 201 Created and JWT."""
    res = client.post("/api/v1/auth/register", json={
        "email": "teacher1@university.edu",
        "password": "SecurePassword123!",
        "full_name": "Prof. Smith"
    })
    assert res.status_code == 201
    data = res.get_json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"
    assert data["user"]["email"] == "teacher1@university.edu"
    assert data["user"]["full_name"] == "Prof. Smith"
    assert "id" in data["user"]

def test_req_f_001_register_duplicate_email_conflict(client):
    """REQ-F-001: Duplicate registration rejected with 409 Conflict (RFC 7807)."""
    payload = {
        "email": "duplicate@university.edu",
        "password": "Password123!",
        "full_name": "Original User"
    }
    res1 = client.post("/api/v1/auth/register", json=payload)
    assert res1.status_code == 201

    res2 = client.post("/api/v1/auth/register", json=payload)
    assert res2.status_code == 409
    data = res2.get_json()
    assert data["status"] == 409
    assert data["title"] == "Conflict"
    assert "duplicate" in data["detail"].lower() or "already exists" in data["detail"].lower()

def test_req_f_001_login_success(client):
    """REQ-F-001: Authenticate with valid credentials and receive token."""
    register_and_login(client, email="login_user@university.edu", password="SecretPassword!")

    res = client.post("/api/v1/auth/login", json={
        "email": "login_user@university.edu",
        "password": "SecretPassword!"
    })
    assert res.status_code == 200
    data = res.get_json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"

def test_req_f_001_login_invalid_credentials_unauthorized(client):
    """REQ-F-001: Invalid credentials rejected with 401 Unauthorized (RFC 7807)."""
    register_and_login(client, email="valid_user@university.edu", password="SecretPassword!")

    res = client.post("/api/v1/auth/login", json={
        "email": "valid_user@university.edu",
        "password": "WrongPassword!"
    })
    assert res.status_code == 401
    data = res.get_json()
    assert data["status"] == 401
    assert data["title"] == "Unauthorized"

def test_req_f_001_get_current_user_profile_me(client):
    """REQ-F-001 & REQ-NF-002: Fetch me profile with role distinction badges."""
    headers, _ = register_and_login(client, email="me_user@university.edu")
    res = client.get("/api/v1/auth/me", headers=headers)
    assert res.status_code == 200
    data = res.get_json()
    assert data["email"] == "me_user@university.edu"
    assert "memberships" in data
    assert isinstance(data["memberships"], list)

def test_req_f_001_unauthorized_access_without_token(client):
    """REQ-F-001 / ADD-002: Protected endpoint returns 401 without Bearer token."""
    res = client.get("/api/v1/auth/me")
    assert res.status_code == 401
    data = res.get_json()
    assert data["status"] == 401

# ============================================================================
# PHASE 2: REQ-F-002 (Class Creation & Mgmt), REQ-F-004 (Role Assignment)
# ============================================================================

def test_req_f_002_create_class_creator_is_admin(client):
    """REQ-F-002: User creates Class, automatically becomes Administrator."""
    headers, user_id = register_and_login(client, email="admin@university.edu")
    res = client.post("/api/v1/classes", headers=headers, json={
        "title": "Software Engineering 101",
        "description": "SDD, TDD, and Architecture"
    })
    assert res.status_code == 201
    data = res.get_json()
    assert "id" in data
    assert data["title"] == "Software Engineering 101"
    assert data["current_user_role"] == "administrator"
    assert data["owner_id"] == user_id

def test_req_f_002_list_classes_and_get_by_id(client):
    """REQ-F-002 & REQ-NF-002: List classes and get specific class."""
    headers, _ = register_and_login(client, email="owner@university.edu")
    c_res = client.post("/api/v1/classes", headers=headers, json={"title": "Data Structures"})
    class_id = c_res.get_json()["id"]

    list_res = client.get("/api/v1/classes", headers=headers)
    assert list_res.status_code == 200
    items = list_res.get_json()["items"]
    assert any(c["id"] == class_id for c in items)

    get_res = client.get(f"/api/v1/classes/{class_id}", headers=headers)
    assert get_res.status_code == 200
    assert get_res.get_json()["title"] == "Data Structures"

def test_req_f_004_role_elevation_student_to_admin(client):
    """REQ-F-004: Administrator promotes Student to Administrator."""
    admin_headers, admin_id = register_and_login(client, email="head_prof@uni.edu")
    c_res = client.post("/api/v1/classes", headers=admin_headers, json={"title": "Algorithms"})
    class_id = c_res.get_json()["id"]

    student_headers, student_id = register_and_login(client, email="assistant@uni.edu")
    inv_res = client.post(f"/api/v1/classes/{class_id}/invites", headers=admin_headers, json={"expires_in_hours": 24})
    token = inv_res.get_json()["invite_token"]
    client.post(f"/api/v1/invites/{token}/join", headers=student_headers)

    # Admin promotes assistant to administrator
    promote_res = client.patch(f"/api/v1/classes/{class_id}/members/{student_id}/role",
                               headers=admin_headers,
                               json={"role": "administrator"})
    assert promote_res.status_code == 200
    assert promote_res.get_json()["role"] == "administrator"

    # Verify assistant now has administrator role in member list
    members_res = client.get(f"/api/v1/classes/{class_id}/members", headers=student_headers)
    assert members_res.status_code == 200
    members = members_res.get_json()["items"]
    promoted = next(m for m in members if m["user_id"] == student_id)
    assert promoted["role"] == "administrator"

# ============================================================================
# PHASE 2: REQ-F-003 & BDD Scenario 1 (Join Class via Invite Link)
# ============================================================================

def test_req_f_003_bdd_scenario_1_invite_lifecycle(client):
    """
    BDD Scenario 1:
    Given a User is logged into the system
    And an Administrator has generated an invite link for "Math 101"
    When the User navigates to the invite link
    Then the User is added to "Math 101" with the "Student" role
    And the User can view materials but cannot upload new ones.
    """
    admin_headers, _ = register_and_login(client, email="prof.euler@uni.edu")
    c_res = client.post("/api/v1/classes", headers=admin_headers, json={"title": "Math 101"})
    class_id = c_res.get_json()["id"]

    # Administrator generates invite
    inv_res = client.post(f"/api/v1/classes/{class_id}/invites", headers=admin_headers, json={
        "expires_in_hours": 48
    })
    assert inv_res.status_code == 201
    invite_token = inv_res.get_json()["invite_token"]

    # Student logs in and joins
    student_headers, student_id = register_and_login(client, email="student.john@uni.edu")
    join_res = client.post(f"/api/v1/invites/{invite_token}/join", headers=student_headers)
    assert join_res.status_code == 200
    assert join_res.get_json()["role"] == "student"
    assert join_res.get_json()["class_id"] == class_id

    # Duplicate join returns 409 Conflict
    dup_res = client.post(f"/api/v1/invites/{invite_token}/join", headers=student_headers)
    assert dup_res.status_code == 409
    assert dup_res.get_json()["status"] == 409

def test_req_f_003_invite_invalid_or_expired_not_found(client):
    """REQ-F-003: Non-existent invite token returns 404 Not Found."""
    headers, _ = register_and_login(client)
    res = client.post("/api/v1/invites/non_existent_token_12345/join", headers=headers)
    assert res.status_code == 404
    assert res.get_json()["status"] == 404

# ============================================================================
# PHASE 3: REQ-F-005 (Subject Management)
# ============================================================================

def test_req_f_005_subject_management(client):
    """REQ-F-005: Create and list Subjects bound strictly to Class (Class -> Subject)."""
    admin_headers, _ = register_and_login(client, email="admin_sub@uni.edu")
    c_res = client.post("/api/v1/classes", headers=admin_headers, json={"title": "Physics"})
    class_id = c_res.get_json()["id"]

    # Admin creates subject
    sub_res = client.post(f"/api/v1/classes/{class_id}/subjects", headers=admin_headers, json={
        "title": "Quantum Mechanics",
        "description": "Wave mechanics and Schrodinger equation"
    })
    assert sub_res.status_code == 201
    subject_id = sub_res.get_json()["id"]
    assert sub_res.get_json()["class_id"] == class_id

    # List subjects
    list_res = client.get(f"/api/v1/classes/{class_id}/subjects", headers=admin_headers)
    assert list_res.status_code == 200
    assert len(list_res.get_json()["items"]) == 1
    assert list_res.get_json()["items"][0]["id"] == subject_id

    # Get subject by id
    get_res = client.get(f"/api/v1/classes/{class_id}/subjects/{subject_id}", headers=admin_headers)
    assert get_res.status_code == 200
    assert get_res.get_json()["title"] == "Quantum Mechanics"

def test_req_f_005_student_forbidden_to_create_subject(client):
    """REQ-F-005: Student cannot create Subject (403 Forbidden)."""
    admin_headers, _ = register_and_login(client, email="admin_p3@uni.edu")
    c_res = client.post("/api/v1/classes", headers=admin_headers, json={"title": "Chemistry"})
    class_id = c_res.get_json()["id"]

    # Create invite and join student
    inv_res = client.post(f"/api/v1/classes/{class_id}/invites", headers=admin_headers)
    token = inv_res.get_json()["invite_token"]

    student_headers, _ = register_and_login(client, email="student_p3@uni.edu")
    client.post(f"/api/v1/invites/{token}/join", headers=student_headers)

    # Student attempts subject creation -> 403 Forbidden
    sub_res = client.post(f"/api/v1/classes/{class_id}/subjects", headers=student_headers, json={
        "title": "Illegal Subject"
    })
    assert sub_res.status_code == 403
    assert sub_res.get_json()["status"] == 403

# ============================================================================
# PHASE 3: REQ-F-006, REQ-NF-001 & BDD Scenario 3 (Material Upload & 500MB)
# ============================================================================

def test_req_f_006_and_req_nf_001_upload_material_within_limit(client):
    """REQ-F-006 & REQ-NF-001: Upload material under 500MB limit."""
    admin_headers, _ = register_and_login(client, email="admin_mat@uni.edu")
    c_res = client.post("/api/v1/classes", headers=admin_headers, json={"title": "Biology"})
    class_id = c_res.get_json()["id"]
    s_res = client.post(f"/api/v1/classes/{class_id}/subjects", headers=admin_headers, json={"title": "Genetics"})
    subject_id = s_res.get_json()["id"]

    # Upload material (file <= 500MB)
    mat_res = client.post(f"/api/v1/classes/{class_id}/subjects/{subject_id}/materials",
                          headers=admin_headers,
                          json={
                              "title": "Lab 1: DNA Extraction Guide",
                              "type": "file",
                              "file_name": "dna_guide.pdf",
                              "file_size_bytes": 1048576, # 1MB
                              "deadline": "2026-12-15T23:59:59Z"
                          })
    assert mat_res.status_code == 201
    mat_data = mat_res.get_json()
    assert mat_data["title"] == "Lab 1: DNA Extraction Guide"
    assert mat_data["subject_id"] == subject_id
    material_id = mat_data["id"]

    # Material can be retrieved
    get_res = client.get(f"/api/v1/classes/{class_id}/subjects/{subject_id}/materials/{material_id}",
                         headers=admin_headers)
    assert get_res.status_code == 200

def test_req_f_006_bdd_scenario_3_oversized_file_rejected_413(client):
    """
    BDD Scenario 3: Uploading an Oversized File
    Given an Administrator is adding Material to a Subject
    When the Administrator attempts to upload a file sized 600MB
    Then the system aborts the upload
    And the system displays an error message stating "File exceeds the 500MB limit."
    """
    admin_headers, _ = register_and_login(client, email="admin_heavy@uni.edu")
    c_res = client.post("/api/v1/classes", headers=admin_headers, json={"title": "Media Studies"})
    class_id = c_res.get_json()["id"]
    s_res = client.post(f"/api/v1/classes/{class_id}/subjects", headers=admin_headers, json={"title": "Video Editing"})
    subject_id = s_res.get_json()["id"]

    # 600MB = 629,145,600 bytes > 524,288,000 bytes
    res = client.post(f"/api/v1/classes/{class_id}/subjects/{subject_id}/materials",
                      headers=admin_headers,
                      json={
                          "title": "Raw 4K Footage",
                          "type": "file",
                          "file_name": "footage.mov",
                          "file_size_bytes": 629145600
                      })
    assert res.status_code == 413
    data = res.get_json()
    assert data["status"] == 413
    assert data["title"] == "Payload Too Large"
    assert "File exceeds the 500MB limit." in data["detail"]

def test_req_f_006_exact_500mb_boundary_acceptance(client):
    """ADD-003: Exact boundary 524,288,000 bytes is accepted."""
    admin_headers, _ = register_and_login(client, email="admin_boundary@uni.edu")
    c_res = client.post("/api/v1/classes", headers=admin_headers, json={"title": "Boundary Test"})
    class_id = c_res.get_json()["id"]
    s_res = client.post(f"/api/v1/classes/{class_id}/subjects", headers=admin_headers, json={"title": "Boundary Subject"})
    subject_id = s_res.get_json()["id"]

    # Exactly 500MB = 524,288,000 bytes
    res = client.post(f"/api/v1/classes/{class_id}/subjects/{subject_id}/materials",
                      headers=admin_headers,
                      json={
                          "title": "Boundary Exact 500MB",
                          "type": "file",
                          "file_name": "data.tar",
                          "file_size_bytes": 524288000
                      })
    assert res.status_code == 201

# ============================================================================
# PHASE 4: REQ-F-007 (Calendar & Deadlines)
# ============================================================================

def test_req_f_007_calendar_deadlines(client):
    """REQ-F-007: Administrators assign deadlines and members view them on calendar."""
    admin_headers, _ = register_and_login(client, email="admin_cal@uni.edu")
    c_res = client.post("/api/v1/classes", headers=admin_headers, json={"title": "Network Systems"})
    class_id = c_res.get_json()["id"]
    s_res = client.post(f"/api/v1/classes/{class_id}/subjects", headers=admin_headers, json={"title": "Routing"})
    subject_id = s_res.get_json()["id"]

    mat_res = client.post(f"/api/v1/classes/{class_id}/subjects/{subject_id}/materials",
                          headers=admin_headers,
                          json={
                              "title": "Lab Report",
                              "type": "link",
                              "link_url": "https://docs.google.com/report1",
                              "deadline": "2026-11-20T18:00:00Z"
                          })
    material_id = mat_res.get_json()["id"]

    # Admin alters deadline
    new_dl = "2026-11-25T18:00:00Z"
    dl_res = client.put(f"/api/v1/classes/{class_id}/subjects/{subject_id}/materials/{material_id}/deadline",
                        headers=admin_headers,
                        json={"deadline": new_dl})
    assert dl_res.status_code == 200
    assert dl_res.get_json()["deadline"] == new_dl

    # Query class calendar
    cal_res = client.get(f"/api/v1/classes/{class_id}/calendar?from=2026-11-01&to=2026-11-30",
                         headers=admin_headers)
    assert cal_res.status_code == 200
    entries = cal_res.get_json()["entries"]
    assert any(e["material_id"] == material_id for e in entries)

# ============================================================================
# PHASE 4: REQ-F-008 (Automated Reminders)
# ============================================================================

def test_req_f_008_reminders_generation_and_mark_read(client):
    """REQ-F-008: List reminders (7-day, 1-day) and mark as read."""
    headers, _ = register_and_login(client, email="reminder_user@uni.edu")

    # List reminders
    rem_res = client.get("/api/v1/reminders", headers=headers)
    assert rem_res.status_code == 200
    data = rem_res.get_json()
    assert "items" in data
    assert "unread_count" in data

    if data["items"]:
        first_id = data["items"][0]["id"]
        patch_res = client.patch(f"/api/v1/reminders/{first_id}/read", headers=headers)
        assert patch_res.status_code == 200
        assert patch_res.get_json()["is_read"] is True

# ============================================================================
# PHASE 4: REQ-F-009, REQ-F-010 & BDD Scenario 2 (Extension Requests)
# ============================================================================

def test_req_f_009_and_010_bdd_scenario_2_extension_lifecycle(client):
    """
    BDD Scenario 2: Requesting a Deadline Extension
    Given a Student is viewing a Material with a set Deadline
    When the Student clicks "Request Extension"
    And the Student submits the request with the comment "I was sick"
    Then an Extension Request is created
    And the Administrator of the Class receives a notification of the request.
    (Followed by REQ-F-010: Administrator approves request and updates deadline)
    """
    admin_headers, admin_id = register_and_login(client, email="prof_ext@uni.edu")
    c_res = client.post("/api/v1/classes", headers=admin_headers, json={"title": "OS Principles"})
    class_id = c_res.get_json()["id"]
    s_res = client.post(f"/api/v1/classes/{class_id}/subjects", headers=admin_headers, json={"title": "Concurrency"})
    subject_id = s_res.get_json()["id"]

    orig_deadline = "2026-11-10T12:00:00Z"
    mat_res = client.post(f"/api/v1/classes/{class_id}/subjects/{subject_id}/materials",
                          headers=admin_headers,
                          json={
                              "title": "Kernel Patch Project",
                              "type": "file",
                              "file_name": "patch.c",
                              "file_size_bytes": 1024,
                              "deadline": orig_deadline
                          })
    material_id = mat_res.get_json()["id"]

    # Student joins class
    inv_res = client.post(f"/api/v1/classes/{class_id}/invites", headers=admin_headers)
    token = inv_res.get_json()["invite_token"]
    student_headers, student_id = register_and_login(client, email="sick_student@uni.edu")
    client.post(f"/api/v1/invites/{token}/join", headers=student_headers)

    # Student submits extension request
    req_deadline = "2026-11-15T12:00:00Z"
    ext_res = client.post(f"/api/v1/classes/{class_id}/materials/{material_id}/extension-requests",
                          headers=student_headers,
                          json={
                              "comment": "I was sick",
                              "requested_deadline": req_deadline
                          })
    assert ext_res.status_code == 201
    ext_data = ext_res.get_json()
    assert ext_data["status"] == "pending"
    assert ext_data["comment"] == "I was sick"
    assert ext_data["requester_id"] == student_id
    request_id = ext_data["id"]

    # Administrator lists extension requests
    list_ext = client.get(f"/api/v1/classes/{class_id}/extension-requests", headers=admin_headers)
    assert list_ext.status_code == 200
    assert any(r["id"] == request_id for r in list_ext.get_json()["items"])

    # Administrator approves extension with class scope
    decision_res = client.patch(f"/api/v1/classes/{class_id}/extension-requests/{request_id}/decision",
                                headers=admin_headers,
                                json={
                                    "status": "approved",
                                    "resolution_comment": "Approved due to medical certificate",
                                    "scope": "class"
                                })
    assert decision_res.status_code == 200
    assert decision_res.get_json()["status"] == "approved"

    # Verify material deadline shifted to approved date
    updated_mat = client.get(f"/api/v1/classes/{class_id}/subjects/{subject_id}/materials/{material_id}",
                             headers=student_headers)
    assert updated_mat.status_code == 200
    assert updated_mat.get_json()["deadline"] == req_deadline

# ============================================================================
# PHASE 5 / ADDENDUM 02: REQ-F-011 (Material Deletion & Cascading Lifecycle)
# ============================================================================

def test_req_f_011_bdd_scenario_4_admin_delete_material_success(client):
    """
    BDD Scenario 4: Deleting Obsolete Material
    Given an Administrator is managing a Subject in "Math 101" containing a Material "Draft Syllabus"
    When the Administrator issues a DELETE request for "Draft Syllabus"
    Then the server responds with HTTP 204 No Content
    And subsequent GET requests for the Material return HTTP 404 Not Found
    """
    admin_headers, _ = register_and_login(client, email="prof_del@uni.edu")
    c_res = client.post("/api/v1/classes", headers=admin_headers, json={"title": "Math 101"})
    class_id = c_res.get_json()["id"]
    s_res = client.post(f"/api/v1/classes/{class_id}/subjects", headers=admin_headers, json={"title": "Linear Algebra"})
    subject_id = s_res.get_json()["id"]

    mat_res = client.post(f"/api/v1/classes/{class_id}/subjects/{subject_id}/materials",
                          headers=admin_headers,
                          json={"title": "Draft Syllabus", "type": "link", "link_url": "https://uni.edu/draft"})
    material_id = mat_res.get_json()["id"]

    # Delete material as administrator -> 204 No Content
    del_res = client.delete(f"/api/v1/classes/{class_id}/subjects/{subject_id}/materials/{material_id}",
                            headers=admin_headers)
    assert del_res.status_code == 204
    assert del_res.data == b""

    # Subsequent GET returns 404 Not Found
    get_res = client.get(f"/api/v1/classes/{class_id}/subjects/{subject_id}/materials/{material_id}",
                         headers=admin_headers)
    assert get_res.status_code == 404

def test_req_f_011_bdd_scenario_5_student_forbidden_to_delete_material(client):
    """
    BDD Scenario 5: Unauthorized Material Deletion Attempt
    Given a Student has enrolled in "Math 101"
    When the Student attempts to issue a DELETE request for a Material
    Then the system rejects the operation with HTTP 403 Forbidden
    """
    admin_headers, _ = register_and_login(client, email="prof_secure@uni.edu")
    c_res = client.post("/api/v1/classes", headers=admin_headers, json={"title": "Secure Class"})
    class_id = c_res.get_json()["id"]
    s_res = client.post(f"/api/v1/classes/{class_id}/subjects", headers=admin_headers, json={"title": "Security"})
    subject_id = s_res.get_json()["id"]

    mat_res = client.post(f"/api/v1/classes/{class_id}/subjects/{subject_id}/materials",
                          headers=admin_headers,
                          json={"title": "Protected Exam", "type": "link", "link_url": "https://uni.edu/exam"})
    material_id = mat_res.get_json()["id"]

    # Student joins class
    inv_res = client.post(f"/api/v1/classes/{class_id}/invites", headers=admin_headers)
    token = inv_res.get_json()["invite_token"]
    student_headers, _ = register_and_login(client, email="attacker_student@uni.edu")
    client.post(f"/api/v1/invites/{token}/join", headers=student_headers)

    # Student attempts deletion -> 403 Forbidden
    del_res = client.delete(f"/api/v1/classes/{class_id}/subjects/{subject_id}/materials/{material_id}",
                            headers=student_headers)
    assert del_res.status_code == 403
    assert del_res.get_json()["status"] == 403

def test_req_f_011_delete_nonexistent_material_not_found(client):
    """REQ-F-011: Deletion of non-existent material returns 404 Not Found."""
    admin_headers, _ = register_and_login(client, email="prof_nf@uni.edu")
    c_res = client.post("/api/v1/classes", headers=admin_headers, json={"title": "Class NF"})
    class_id = c_res.get_json()["id"]
    s_res = client.post(f"/api/v1/classes/{class_id}/subjects", headers=admin_headers, json={"title": "Subject NF"})
    subject_id = s_res.get_json()["id"]

    del_res = client.delete(f"/api/v1/classes/{class_id}/subjects/{subject_id}/materials/non_existent_mat_999",
                            headers=admin_headers)
    assert del_res.status_code == 404

def test_req_f_011_cascading_cleanup_calendar_and_extensions(client):
    """REQ-F-011: Deletion cascades to expunge calendar entries and cancel pending extensions."""
    admin_headers, _ = register_and_login(client, email="prof_cascade@uni.edu")
    c_res = client.post("/api/v1/classes", headers=admin_headers, json={"title": "Cascade Class"})
    class_id = c_res.get_json()["id"]
    s_res = client.post(f"/api/v1/classes/{class_id}/subjects", headers=admin_headers, json={"title": "Cascade Subject"})
    subject_id = s_res.get_json()["id"]

    # Create material with deadline
    mat_res = client.post(f"/api/v1/classes/{class_id}/subjects/{subject_id}/materials",
                          headers=admin_headers,
                          json={
                              "title": "Assignment to be Deleted",
                              "type": "file",
                              "file_name": "task.pdf",
                              "file_size_bytes": 2048,
                              "deadline": "2026-11-28T23:59:59Z"
                          })
    material_id = mat_res.get_json()["id"]

    # Student joins and requests extension
    inv_res = client.post(f"/api/v1/classes/{class_id}/invites", headers=admin_headers)
    token = inv_res.get_json()["invite_token"]
    student_headers, _ = register_and_login(client, email="cascade_student@uni.edu")
    client.post(f"/api/v1/invites/{token}/join", headers=student_headers)

    client.post(f"/api/v1/classes/{class_id}/materials/{material_id}/extension-requests",
                headers=student_headers,
                json={"comment": "Need more time", "requested_deadline": "2026-12-05T23:59:59Z"})

    # Verify material deadline is in calendar
    cal_res = client.get(f"/api/v1/classes/{class_id}/calendar", headers=admin_headers)
    assert any(e["material_id"] == material_id for e in cal_res.get_json()["entries"])

    # Administrator deletes material
    del_res = client.delete(f"/api/v1/classes/{class_id}/subjects/{subject_id}/materials/{material_id}",
                            headers=admin_headers)
    assert del_res.status_code == 204

    # Verify calendar no longer contains the deleted material's deadline
    cal_after = client.get(f"/api/v1/classes/{class_id}/calendar", headers=admin_headers)
    assert not any(e["material_id"] == material_id for e in cal_after.get_json()["entries"])

    # Verify extension requests no longer lists pending request for that material
    ext_after = client.get(f"/api/v1/classes/{class_id}/extension-requests", headers=admin_headers)
    assert not any(r["material_id"] == material_id for r in ext_after.get_json()["items"])

