# SRS Addendum: REST API Behavioral Clarifications & Architectural Decisions

**Project:** LabManager  
**Document Version:** 1.0 (Addendum to SRS v1.0)  
**Date:** 2026-10-24  
**Author:** AI Coding Agent  
**Auditor:** Human Reviewer  

---

## 1. Purpose of Addendum

This addendum formalizes behavioral, protocol-level, and data model clarifications established during the API-first design phase (Laboratory Work #4). These decisions do not alter the business scope approved in SRS v1.0, but translate high-level requirements into an unambiguous REST API contract.

---

## 2. Formal Behavioral Refinements

### ADD-001: Standardized Error Representation (RFC 7807 / RFC 9457)
- **SRS Reference:** All requirements involving validation or rejection (`REQ-F-001`, `REQ-F-003`, `REQ-F-006`, `REQ-NF-001`).
- **Clarification:** All HTTP errors (4xx, 5xx) must return `Content-Type: application/problem+json` containing:
  - `type` (URI identifier of the problem class)
  - `title` (short human-readable summary)
  - `status` (HTTP status code)
  - `detail` (context-specific failure reason)
  - `instance` (request URI path)
  - `invalid_params` (array of offending field names and specific validation errors).

### ADD-002: Authentication & Contextual Authorization Protocol
- **SRS Reference:** `REQ-F-001`, `REQ-NF-002`.
- **Clarification:** The API adopts stateless JWT (JSON Web Tokens) passed via standard HTTP header `Authorization: Bearer <jwt_token>`. The token encodes user identity. User permissions are contextual per Class (`administrator` vs `student`), verified against membership records upon each protected operation.

### ADD-003: Exact Byte Threshold for File Attachments (REQ-NF-001)
- **SRS Reference:** `REQ-NF-001`, `REQ-F-006` (BDD Scenario 3).
- **Clarification:** The 500MB storage ceiling is strictly enforced as $500 \times 1024 \times 1024 = 524,288,000$ bytes. Any upload exceeding this limit is rejected with HTTP `413 Payload Too Large` and detail message `"File exceeds the 500MB limit."`.

### ADD-004: Calendar Temporal Query Parameters
- **SRS Reference:** `REQ-F-007`.
- **Clarification:** The calendar endpoint (`GET /api/v1/classes/{classId}/calendar` and `GET /api/v1/calendar`) accepts optional ISO-8601 query parameters `from` and `to` (format: `YYYY-MM-DD`) to allow client-side pagination and efficient month/week view rendering.

### ADD-005: Invite Token Expiration & Usage Lifecycle
- **SRS Reference:** `REQ-F-003` (BDD Scenario 1).
- **Clarification:** Generated invite tokens default to a validity window of 168 hours (7 days), configurable up to 720 hours (30 days). Expired tokens return `404 Not Found` with problem detail `"Invite token has expired"`. Duplicate join attempts by existing members return `409 Conflict`.

### ADD-006: Extension Request Resolution Scoping
- **SRS Reference:** `REQ-F-010`.
- **Clarification:** The approval payload accepts `scope: "user" | "class"` (defaulting to `"user"`). When `scope: "class"`, the new deadline timestamp cascades to all enrolled members of that Class for the associated Material.
