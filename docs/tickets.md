# Decomposition of Requirements into SDD Tickets

**Project:** LabManager  
**Source Specification:** `spec/srs.md` (v1.0)  
**Tracking System:** GitHub Issues & Projects  

---

## 1. Ticket Decomposition Overview

Every ticket directly originates from an approved SRS requirement or is a structural Gate/Verification task required by the SDD lifecycle. No extraneous scope has been introduced.

| Ticket ID | Type | SRS Ref | Title / Scope | Assigned Role | Dependencies (Blocked By) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TICK-001** | `Gate` | Baseline | **PLAN-GATE: Approval of Decomposition & Execution Plan** | Human Reviewer | All decomposition artifacts |
| **TICK-002** | `Test` | REQ-F-001 | Auth & User Account Test Suite (Unit & BDD) | AI Coding Agent | TICK-001 |
| **TICK-003** | `Feature` | REQ-F-001 | User Registration, Authentication & Profile Backend/UI | AI Coding Agent | TICK-002 |
| **TICK-004** | `Test` | REQ-F-002, REQ-F-004 | Class & Permissions Context Test Suite | AI Coding Agent | TICK-003 |
| **TICK-005** | `Feature` | REQ-F-002 | Class Creation & Admin Ownership Module | AI Coding Agent | TICK-004 |
| **TICK-006** | `Feature` | REQ-F-004 | Contextual Role Assignment & Elevation Module | AI Coding Agent | TICK-005 |
| **TICK-007** | `Test` | REQ-F-003 | Class Joining via Invite Link Test Suite (BDD Scenario 1) | AI Coding Agent | TICK-005 |
| **TICK-008** | `Feature` | REQ-F-003 | Invite Link Generator & Student Join Flow | AI Coding Agent | TICK-007 |
| **TICK-009** | `Test` | REQ-F-005 | Subject Hierarchy & Containment Test Suite | AI Coding Agent | TICK-005 |
| **TICK-010** | `Feature` | REQ-F-005 | Subject Management Module (Class -> Subject) | AI Coding Agent | TICK-009 |
| **TICK-011** | `Test` | REQ-F-006, REQ-NF-001 | Material Upload & 500MB Limit Test Suite (BDD Scenario 3) | AI Coding Agent | TICK-010 |
| **TICK-012** | `Feature` | REQ-F-006, REQ-NF-001 | File & Link Attachment Service with 500MB Validation | AI Coding Agent | TICK-011 |
| **TICK-013** | `Test` | REQ-F-007 | Calendar & Deadline Association Test Suite | AI Coding Agent | TICK-012 |
| **TICK-014** | `Feature` | REQ-F-007 | Built-in Calendar Component & Deadline Visualization | AI Coding Agent | TICK-013 |
| **TICK-015** | `Test` | REQ-F-008 | Scheduled Reminders Notification Engine Test Suite | AI Coding Agent | TICK-014 |
| **TICK-016** | `Feature` | REQ-F-008 | Internal Reminder Service (7-Day & 1-Day Triggers) | AI Coding Agent | TICK-015 |
| **TICK-017** | `Test` | REQ-F-009, REQ-F-010 | Extension Request & Approval Lifecycle Tests (BDD Scenario 2) | AI Coding Agent | TICK-014 |
| **TICK-018** | `Feature` | REQ-F-009 | Student Extension Request Form & Notification Handler | AI Coding Agent | TICK-017 |
| **TICK-019** | `Feature` | REQ-F-010 | Admin Extension Decision (Approve/Reject) & Deadline Shifter | AI Coding Agent | TICK-018 |
| **TICK-020** | `Feature` | REQ-NF-002 | UI Role Distinction (Admin vs Student Visual Theme/Badging) | AI Coding Agent | TICK-006, TICK-008 |
| **TICK-021** | `Verification` | All | Automated Full-Suite Verification & Linting Pipeline | AI Coding Agent | TICK-003, TICK-006, TICK-008, TICK-010, TICK-012, TICK-014, TICK-016, TICK-019, TICK-020 |
| **TICK-022** | `Documentation` | All | User Guide, API Documentation & Architecture Manual | AI Coding Agent | TICK-021 |
| **TICK-023** | `Validation` | REQ-NF-002, All | User Acceptance Testing (UAT) & Usability Validation | Human Reviewer | TICK-021 |
| **TICK-024** | `Gate` | All | **STAGE-GATE: Final Release & Delivery Sign-Off** | Human Reviewer | TICK-022, TICK-023 |

---

## 2. Detailed Ticket Specifications

### TICK-001: PLAN-GATE Approval
- **Type:** `Gate`
- **Role:** Human Reviewer
- **Inputs:** `spec/srs.md`, `docs/tickets.md`, `docs/plan.md`, `docs/risks.md`, `docs/traceability_matrix.md`.
- **Criteria:** Plan fully maps to requirements without scope creep. Human approves plan with `GO` decision.

### TICK-002: Auth & User Account Test Suite
- **Type:** `Test`
- **Role:** AI Coding Agent
- **Requirement:** REQ-F-001
- **Criteria:** Unit tests for user creation, password hashing, JWT token issue/validation, invalid credentials handling.

### TICK-003: User Registration, Auth & Profile
- **Type:** `Feature`
- **Role:** AI Coding Agent
- **Requirement:** REQ-F-001
- **Criteria:** User can register with email and password, log in, and view main dashboard. Tests in TICK-002 pass 100%.

### TICK-004: Class & Permissions Context Test Suite
- **Type:** `Test`
- **Role:** AI Coding Agent
- **Requirement:** REQ-F-002, REQ-F-004
- **Criteria:** Tests verify that creator becomes Admin, and Admin can grant permissions to another user.

### TICK-005: Class Creation & Admin Ownership Module
- **Type:** `Feature`
- **Role:** AI Coding Agent
- **Requirement:** REQ-F-002
- **Criteria:** User clicks "Create Class", supplies title, becomes Class Administrator with edit permissions.

### TICK-006: Contextual Role Assignment & Elevation Module
- **Type:** `Feature`
- **Role:** AI Coding Agent
- **Requirement:** REQ-F-004
- **Criteria:** Administrator can promote any Student to Administrator within that Class.

### TICK-007: Class Joining via Invite Link Test Suite
- **Type:** `Test`
- **Role:** AI Coding Agent
- **Requirement:** REQ-F-003 (BDD Scenario 1)
- **Criteria:** Tests verify link token validation, joining with read-only Student role.

### TICK-008: Invite Link Generator & Student Join Flow
- **Type:** `Feature`
- **Role:** AI Coding Agent
- **Requirement:** REQ-F-003
- **Criteria:** Admin generates invite link; clicking link adds user as Student with read-only access.

### TICK-009: Subject Hierarchy Test Suite
- **Type:** `Test`
- **Role:** AI Coding Agent
- **Requirement:** REQ-F-005
- **Criteria:** Tests verify strict parent-child binding (`Class -> Subject`) and permission enforcement.

### TICK-010: Subject Management Module
- **Type:** `Feature`
- **Role:** AI Coding Agent
- **Requirement:** REQ-F-005
- **Criteria:** Admin creates and organizes Subjects under their Class.

### TICK-011: Material Upload & 500MB Limit Test Suite
- **Type:** `Test`
- **Role:** AI Coding Agent
- **Requirement:** REQ-F-006, REQ-NF-001 (BDD Scenario 3)
- **Criteria:** Tests verify acceptance of <= 500MB (images, text, archives, code), reject > 500MB with error message.

### TICK-012: Material Attachment Service with 500MB Validation
- **Type:** `Feature`
- **Role:** AI Coding Agent
- **Requirement:** REQ-F-006, REQ-NF-001
- **Criteria:** Admin uploads files or links; file size limit enforced; files attached strictly to chosen Subject.

### TICK-013: Calendar & Deadline Test Suite
- **Type:** `Test`
- **Role:** AI Coding Agent
- **Requirement:** REQ-F-007
- **Criteria:** Tests verify timestamp persistence, queries for monthly/weekly deadlines, calendar data feed.

### TICK-014: Built-in Calendar Component & Deadline Visualization
- **Type:** `Feature`
- **Role:** AI Coding Agent
- **Requirement:** REQ-F-007
- **Criteria:** Calendar UI displays active deadlines for all Class members according to date and time.

### TICK-015: Reminders Notification Engine Test Suite
- **Type:** `Test`
- **Role:** AI Coding Agent
- **Requirement:** REQ-F-008
- **Criteria:** Tests verify trigger dispatch at exactly 7 days and 1 day prior to deadline.

### TICK-016: Internal Reminder Service
- **Type:** `Feature`
- **Role:** AI Coding Agent
- **Requirement:** REQ-F-008
- **Criteria:** Background task queries upcoming deadlines and creates dashboard notifications for Class members.

### TICK-017: Extension Request Lifecycle Tests
- **Type:** `Test`
- **Role:** AI Coding Agent
- **Requirement:** REQ-F-009, REQ-F-010 (BDD Scenario 2)
- **Criteria:** Tests student request submission with reason comment, admin approval/rejection state transitions.

### TICK-018: Student Extension Request Form & Notification
- **Type:** `Feature`
- **Role:** AI Coding Agent
- **Requirement:** REQ-F-009
- **Criteria:** Student submits extension request with text comment; Admin receives notification in dashboard.

### TICK-019: Admin Extension Decision & Deadline Shifter
- **Type:** `Feature`
- **Role:** AI Coding Agent
- **Requirement:** REQ-F-010
- **Criteria:** Admin approves or rejects request; approval updates deadline timestamp for student or class.

### TICK-020: UI Role Distinction (Admin vs Student)
- **Type:** `Feature`
- **Role:** AI Coding Agent
- **Requirement:** REQ-NF-002
- **Criteria:** Visual distinctions (color themes, badges, controls visibility) immediately reflect user's contextual role.

### TICK-021: Automated Verification & CI Pipeline
- **Type:** `Verification`
- **Role:** AI Coding Agent
- **Requirement:** Cross-cutting
- **Criteria:** 100% test pass rate across all test suites, zero linter/type errors, clean build.

### TICK-022: Documentation & Manuals
- **Type:** `Documentation`
- **Role:** AI Coding Agent
- **Requirement:** Cross-cutting
- **Criteria:** Updated user guide, system documentation, and traceability references.

### TICK-023: User Acceptance Testing & Intent Validation
- **Type:** `Validation`
- **Role:** Human Reviewer
- **Requirement:** REQ-NF-002, All
- **Criteria:** Human confirms functional satisfaction, UI clarity, and real-world usability.

### TICK-024: Final Stage-Gate (PROD-GATE)
- **Type:** `Gate`
- **Role:** Human Reviewer
- **Requirement:** All
- **Criteria:** Verification passed, validation signed off, documentation complete. Decision = GO for deployment.
