# Stage-Gate Checkpoint: TEST-GATE (Base Implementation)

**Project:** LabManager  
**Date:** 2026-11-06  
**Checkpoint:** **TEST-GATE (Pre-Implementation TDD Gate)**  
**Auditor / Decision Maker:** Human Reviewer & AI Coding Agent  
**Baseline Inputs:**
- SRS v1.0 (`spec/srs.md`)
- SRS Addendum v1.0 (`spec/srs_addendum.md`)
- Approved OpenAPI Specification (`spec/openapi.yaml`, `spec/openapi.json`)
- Decomposition Tickets (`docs/tickets.md`: TICK-002 to TICK-019)
- Test Suite: `tests/test_server_api.py` (19 test cases covering all 12 SRS requirements)

---

## 1. Objective of TEST-GATE

Verify that:
1. Automated tests are derived causally and independently from the specification (SRS, Acceptance Criteria, BDD Scenarios, OpenAPI Contract) before implementation.
2. The tests cover positive, negative, and boundary scenarios.
3. The tests are executed prior to coding and fail (RED phase) strictly due to the absence of the server implementation (`ModuleNotFoundError: No module named 'src.app'`).
4. Logging requirements and modular architecture boundaries are formally defined and enforced.

---

## 2. Test-to-Requirement Verification & Coverage

| Test Function | Requirement(s) | Scenario Type | Expected Pre-Code Status |
| :--- | :--- | :--- | :---: |
| `test_req_f_001_register_user_success` | REQ-F-001 | Positive (User Registration) | **FAIL (RED)** |
| `test_req_f_001_register_duplicate_email_conflict` | REQ-F-001 | Negative (409 Conflict) | **FAIL (RED)** |
| `test_req_f_001_login_success` | REQ-F-001 | Positive (Authentication & JWT) | **FAIL (RED)** |
| `test_req_f_001_login_invalid_credentials_unauthorized` | REQ-F-001 | Negative (401 Unauthorized) | **FAIL (RED)** |
| `test_req_f_001_get_current_user_profile_me` | REQ-F-001, REQ-NF-002 | Positive (Profile & Role Badges) | **FAIL (RED)** |
| `test_req_f_001_unauthorized_access_without_token` | REQ-F-001, ADD-002 | Negative (401 No Token) | **FAIL (RED)** |
| `test_req_f_002_create_class_creator_is_admin` | REQ-F-002 | Positive (Class Ownership) | **FAIL (RED)** |
| `test_req_f_002_list_classes_and_get_by_id` | REQ-F-002, REQ-NF-002 | Positive (Class Hierarchy) | **FAIL (RED)** |
| `test_req_f_004_role_elevation_student_to_admin` | REQ-F-004 | Positive (Contextual Promotion) | **FAIL (RED)** |
| `test_req_f_003_bdd_scenario_1_invite_lifecycle` | REQ-F-003 | BDD Scenario 1 (Invite Join) | **FAIL (RED)** |
| `test_req_f_003_invite_invalid_or_expired_not_found`| REQ-F-003, ADD-005 | Negative (404 Non-existent/Expired) | **FAIL (RED)** |
| `test_req_f_005_subject_management` | REQ-F-005 | Positive (Class -> Subject) | **FAIL (RED)** |
| `test_req_f_005_student_forbidden_to_create_subject` | REQ-F-005 | Negative (403 Forbidden) | **FAIL (RED)** |
| `test_req_f_006_and_req_nf_001_upload_material_within_limit` | REQ-F-006, REQ-NF-001 | Positive (Upload <= 500MB) | **FAIL (RED)** |
| `test_req_f_006_bdd_scenario_3_oversized_file_rejected_413` | REQ-F-006, REQ-NF-001 | BDD Scenario 3 (413 Payload Too Large) | **FAIL (RED)** |
| `test_req_f_006_exact_500mb_boundary_acceptance` | REQ-NF-001, ADD-003 | Boundary (524,288,000 bytes) | **FAIL (RED)** |
| `test_req_f_007_calendar_deadlines` | REQ-F-007, ADD-004 | Positive (Calendar & Dates) | **FAIL (RED)** |
| `test_req_f_008_reminders_generation_and_mark_read` | REQ-F-008 | Positive (7-Day/1-Day Reminders) | **FAIL (RED)** |
| `test_req_f_009_and_010_bdd_scenario_2_extension_lifecycle` | REQ-F-009, REQ-F-010 | BDD Scenario 2 (Extension Workflow) | **FAIL (RED)** |

---

## 3. Pre-Implementation Test Run Diagnostic

- **Command:** `python -m pytest tests/test_server_api.py`
- **Output:** `ModuleNotFoundError: No module named 'src.app'`
- **Conclusion:** Causal independence confirmed. Tests accurately expect the application contract and fail purely because the implementation has not yet been built.

---

## 4. Formal Decision

**Gate Decision:** **GO**  
**Action Unlocked:** Proceed to GREEN phase: implement modular components in `src/` (Core, Logging, Security, Models, Repositories, Services, Controllers, and Flask App Factory).
