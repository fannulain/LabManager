# Traceability Matrix

| Requirement ID | Acceptance Criteria | BDD Scenario | Ticket(s) | Test | Code Module | Documentation |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **REQ-F-001** | Account creation, login, dashboard access. | - | TICK-002, TICK-003 | tests/test_auth.py | src/auth/ | docs/user_guide.md |
| **REQ-F-002** | Class is generated with edit permissions for creator. | - | TICK-004, TICK-005 | tests/test_classes.py | src/classes/ | docs/user_guide.md |
| **REQ-F-003** | User joins via link and receives view-only access. | Scenario 1 | TICK-007, TICK-008 | tests/test_invites.py | src/invites/ | docs/user_guide.md |
| **REQ-F-004** | Target user gains edit permissions upon promotion. | - | TICK-004, TICK-006 | tests/test_roles.py | src/roles/ | docs/user_guide.md |
| **REQ-F-005** | Subject is created under a Class (Class -> Subject). | - | TICK-009, TICK-010 | tests/test_subjects.py | src/subjects/ | docs/user_guide.md |
| **REQ-F-006** | File attached to Subject, respects size limits. | Scenario 3 | TICK-011, TICK-012 | tests/test_materials.py | src/materials/ | docs/user_guide.md |
| **REQ-F-007** | Deadline displayed on the Class calendar view. | - | TICK-013, TICK-014 | tests/test_calendar.py | src/calendar/ | docs/user_guide.md |
| **REQ-F-008** | Notification appears 7 days and 1 day prior. | - | TICK-015, TICK-016 | tests/test_reminders.py | src/reminders/ | docs/user_guide.md |
| **REQ-F-009** | Request submitted and appears in Admin dashboard. | Scenario 2 | TICK-017, TICK-018 | tests/test_extensions.py | src/extensions/ | docs/user_guide.md |
| **REQ-F-010** | Admin approval successfully alters the deadline timestamp. | - | TICK-017, TICK-019 | tests/test_extensions.py | src/extensions/ | docs/user_guide.md |
| **REQ-NF-001** | System accepts <500MB files, rejects >500MB files. | Scenario 3 | TICK-011, TICK-012 | tests/test_materials.py | src/materials/ | docs/user_guide.md |
| **REQ-NF-002** | UI visually separates Admin classes from Student classes. | - | TICK-020, TICK-023 | tests/test_ui_roles.py | src/ui/components/ | docs/user_guide.md |

> *Note: Verification and delivery across all requirements are governed by verification pipeline TICK-021, human intent validation TICK-023, and final release gate TICK-024.*
