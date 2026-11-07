# Stage-Gate Checkpoint: TEST-GATE (Addendum 02)

**Project:** LabManager  
**Date:** 2026-11-06  
**Checkpoint:** **TEST-GATE (Addendum TDD Verification)**  
**Specification Reference:** `spec/srs_addendum_02.md` (REQ-F-011)  
**Auditor / Decision Maker:** Human Reviewer & AI Coding Agent  
**Status:** **APPROVED (GO)**

---

## 1. Objective of TEST-GATE (Addendum)

Verify that:
1. Four new independent tests covering REQ-F-011 and BDD Scenarios 4 & 5 have been created in `tests/test_server_api.py`.
2. The tests were run BEFORE modifying server code.
3. The tests failed with the expected causal reason: `405 METHOD NOT ALLOWED` (Flask route does not support `DELETE`).
4. Regression safety: All 19 existing baseline tests continue to pass without interference.

---

## 2. Test Execution Diagnostic Matrix

| Test Identifier | Scope / Scenario | Expected Diagnostic | Actual Pre-Code Result |
| :--- | :--- | :--- | :---: |
| `test_req_f_011_bdd_scenario_4_admin_delete_material_success` | BDD Scenario 4: Admin deletion -> 204 No Content | Fails with 405 Method Not Allowed | **FAIL (405 != 204)** |
| `test_req_f_011_bdd_scenario_5_student_forbidden_to_delete_material` | BDD Scenario 5: Student deletion attempt -> 403 Forbidden | Fails with 405 Method Not Allowed | **FAIL (405 != 403)** |
| `test_req_f_011_delete_nonexistent_material_not_found` | Non-existent target -> 404 Not Found | Fails with 405 Method Not Allowed | **FAIL (405 != 404)** |
| `test_req_f_011_cascading_cleanup_calendar_and_extensions` | Cascading expunging of calendar & extensions | Fails with 405 Method Not Allowed | **FAIL (405 != 204)** |

---

## 3. Formal Gate Decision

**Decision:** **GO**  
**Action Unlocked:** Proceed to GREEN phase: implement `delete_material` method in `DataStore`, `MaterialService`, and `material_routes.py`, ensure audit logging `MATERIAL_DELETED`, and achieve 100% test pass rate across the full suite.
