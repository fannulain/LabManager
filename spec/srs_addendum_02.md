# SRS Addendum 02: Material Deletion and Cascading Lifecycle Management

**Project:** LabManager  
**Document Version:** 2.0 (Addendum 02 to SRS v1.0)  
**Date:** 2026-11-06  
**Author:** AI Coding Agent  
**Auditor / Approver:** Human Reviewer  
**Gate:** SPEC-ADDENDUM-GATE  
**Status:** **APPROVED (GO)**

---

## 1. Problem Statement & Business Justification

In the initial release of LabManager (SRS v1.0), materials could be uploaded by Administrators (`REQ-F-006`) but could not be removed or deleted. In academic environments, teachers regularly replace syllabi, rectify erroneous uploads, or retract assignments. 

Without a managed deletion mechanism, obsolete materials remain permanently in subjects, cluttering the student dashboard and leaving dangling deadlines in the calendar.

---

## 2. Requirement Specification

### REQ-F-011: Managed Material Deletion
The system shall permit an Administrator to delete an educational Material from a Subject within their Class.

#### Acceptance Criteria:
1. **Endpoint & Method:** `DELETE /api/v1/classes/{classId}/subjects/{subjectId}/materials/{materialId}`.
2. **Access Control:** Only users with the contextual role of `administrator` in the specified Class are permitted to delete Materials. Requests from `student` users must be rejected with HTTP `403 Forbidden` (`application/problem+json`).
3. **Non-Existent Target:** Deletion of an unrecorded or previously deleted material must return HTTP `404 Not Found` (`application/problem+json`).
4. **Cascading Cleanup:** Upon successful deletion:
   - The Material is removed from the Subject listing.
   - Any deadlines associated with the Material are expunged from the Class and Global Calendar.
   - Any pending Extension Requests linked to this Material are cancelled and removed.
   - Any scheduled Reminders for this Material are invalidated.
5. **Success Response:** Successful deletion shall return HTTP `204 No Content` with an empty response body.
6. **Audit Trail:** The deletion event must be logged with level `INFO`, recording the acting `user_id`, `class_id`, `subject_id`, and `material_id`.

---

## 3. Behavior-Driven Development (BDD) Scenario

### Scenario 4: Deleting Obsolete Material (BDD Scenario 4)
**Given** an Administrator is managing a Subject in "Math 101" containing a Material "Draft Syllabus"  
**And** the Material has a deadline and an active reminder  
**When** the Administrator issues a `DELETE` request for "Draft Syllabus"  
**Then** the server responds with HTTP `204 No Content`  
**And** subsequent `GET` requests for the Material return HTTP `404 Not Found`  
**And** the Material's deadline is no longer visible in the Class Calendar.

### Scenario 5: Unauthorized Material Deletion Attempt
**Given** a Student has enrolled in "Math 101"  
**When** the Student attempts to issue a `DELETE` request for a Material in "Math 101"  
**Then** the system rejects the operation with HTTP `403 Forbidden`  
**And** the Material remains intact.

---

## 4. Impact Analysis on Existing Artifacts

| Artifact | Impact Description | Required Action |
| :--- | :--- | :--- |
| `spec/openapi.json` & `.yaml` | Missing `delete` operation on `/classes/{classId}/subjects/{subjectId}/materials/{materialId}`. | Add OpenAPI operation `deleteMaterial` with 204, 401, 403, 404 responses. |
| `docs/tickets.md` | New requirement needs tracking. | Register `TICK-025` (Test) and `TICK-026` (Feature). |
| `docs/traceability_matrix.md` | Traceability gap for `REQ-F-011`. | Map `REQ-F-011` to `TICK-025`, `TICK-026`, and `src/materials/`. |
| `src/storage/store.py` | Need `delete_material` method with cascade cleanup. | Implement atomic removal from memory store. |
| `src/services/material_service.py` | Needs `delete_material` business logic and audit logging. | Implement deletion service method. |
| `src/api/material_routes.py` | Route handler for `DELETE` method missing. | Bind `DELETE` method with role decorator. |
| `tests/test_server_api.py` | Need test coverage for `REQ-F-011`. | Author tests prior to modifying code (TDD Red Phase). |
