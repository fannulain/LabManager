# LabManager (Educational Materials and Laboratory Manager)

An information system designed to organize and optimize the educational process by serving as a centralized hub for tracking academic deadlines and structuring educational materials.

Developed using **Specification-Driven Development (SDD)** and **Test-Driven Development (TDD)** within an AI-augmented engineering pipeline with strict **Human-in-the-Loop** verification and stage-gate control.

---

## 1. Core System Capabilities

- **Unified User Model & Contextual Roles:** Generic user accounts dynamically operating as an **Administrator** (educator/creator with content edit rights) or **Student** (read-only member joined via invite link) depending on class context (`REQ-F-001`, `REQ-F-002`, `REQ-F-003`, `REQ-F-004`).
- **Academic Material Structuring:** Strict hierarchical organization (`Class -> Subject -> Materials`) supporting files up to 500MB (images, text, archives, code) and external links (`REQ-F-005`, `REQ-F-006`, `REQ-NF-001`).
- **Material Lifecycle & Deletion (Addendum 02):** Administrators can permanently delete materials with automated cascading cleanup of calendar deadlines, active reminders, and pending extension requests (`REQ-F-011`).
- **Deadline Tracking & Calendar:** Built-in interactive calendar displaying assignment deadlines for class and user global workspaces (`REQ-F-007`).
- **Automated Reminders:** Internal notification triggers dispatched exactly 7 days and 1 day prior to upcoming deadlines (`REQ-F-008`).
- **Deadline Extension Requests:** Formal workflow enabling students to submit extension requests with comments, which administrators review, approve, or reject (`REQ-F-009`, `REQ-F-010`).
- **Visual Role Distinction:** Dynamic UI themes and badges immediately separating administrative workspaces from student view-only classes (`REQ-NF-002`).
- **Structured System Audit Logging:** Centralized logging of all actions, security authentications, errors, and access checks into `logs/system.log`.
- **RFC 7807 Problem Details:** Uniform standard error payloads across all endpoints (`application/problem+json`).

---

## 2. SDD & TDD Engineering Methodology

The project enforces an immutable requirements contract and formal stage-gates before every code transition:

```
[ SRS v1.0 & OpenAPI Contract ]
              ↓
  [ TEST-GATE: Causal RED Tests ]
              ↓
  [ GREEN: Server Implementation ]
              ↓
  [ Behavior-Preserving Refactoring ]
              ↓
  [ SPEC-ADDENDUM-GATE: REQ-F-011 ]
              ↓
  [ TEST-GATE: Addendum RED (405) ]
              ↓
  [ GREEN: Cascade Deletion Logic ]
              ↓
  [ Verification & Human Validation ]
              ↓
  [ FINAL-GATE: Full GO Decision ]
```

- **Human Reviewer:** Product Owner, Lead Architect, and Quality Auditor. Retains exclusive authority over Stage-Gate decisions (`SPEC-GATE`, `PLAN-GATE`, `API-GATE`, `TEST-GATE`, `SPEC-ADDENDUM-GATE`, `FINAL-GATE`), user intent validation, and requirements baseline approvals.
- **AI Coding Agent (Antigravity):** Autonomous technical partner responsible for specification decomposition, independent test generation, modular server implementation, refactoring, and documentation drafting.

---

## 3. Modular Server Architecture (`src/`)

The backend is built with strict component separation and zero vibe coding:

- **`src/core/` (Core Utilities):**
  - `logging_config.py`: Structured logger and audit trail engine writing to `logs/system.log`.
  - `errors.py`: Custom exceptions and RFC 7807 (`application/problem+json`) problem handlers.
  - `security.py`: Password hashing, stateless token management, and contextual role guards.
  - `responses.py`: Unified paginated response formatters.
- **`src/models/` (Domain Entities):**
  - `entities.py`: Data models matching the domain glossary (`User`, `Class`, `Invite`, `Subject`, `Material`, `Reminder`, `ExtensionRequest`).
- **`src/storage/` (Repository Layer):**
  - `store.py`: In-memory isolated data store with query and cascading cleanup operations.
- **`src/services/` (Business Logic Services):**
  - `auth_service.py`, `class_service.py`, `invite_service.py`, `subject_service.py`, `material_service.py`, `calendar_service.py`, `reminder_service.py`, `extension_service.py`.
- **`src/api/` (REST Controllers / Flask Blueprints):**
  - `auth_routes.py`, `class_routes.py`, `invite_routes.py`, `subject_routes.py`, `material_routes.py`, `calendar_routes.py`, `reminder_routes.py`, `extension_routes.py`.
- **`src/templates/` & `src/static/` (Interactive Web Dashboard):**
  - `index.html`: Responsive Single Page Application (SPA) dashboard built with Tailwind CSS and FontAwesome.
- **`src/app.py`:** Application factory configuring Blueprints, Web UI endpoints, error handlers, and audit logging.

---

## 4. Interactive Graphical Web Interface (Web Dashboard)

LabManager includes a rich, responsive Single Page Application (SPA) served directly at **`http://127.0.0.1:5000/`**. It provides full visual interaction covering 100% of the functional and non-functional requirements:

- **Authentication & User Identity (`REQ-F-001`):** Seamless registration, login with JWT token storage, quick demo login buttons (Educator Admin vs. Student), and logout.
- **Contextual Role Differentiation (`REQ-NF-002`):**
  - **Administrator Mode:** Purple theme accent with crown badge; provides controls for creating subjects, generating invites, viewing rosters, elevating students to admins, approving/rejecting extensions, and deleting materials.
  - **Student Mode:** Emerald theme accent with graduate badge; provides read-only course exploration, file downloading, calendar deadline tracking, and extension request forms.
- **Class Management & Invite Workflow (`REQ-F-002`, `REQ-F-003`, `BDD Scenario 1`):** Create new classes, generate expiring invite tokens (24h, 7d, 30d), and join classes via invite link/token.
- **Role Elevation Module (`REQ-F-004`):** Interactive member roster modal allowing administrators to promote enrolled students to administrators.
- **Subject & Material Management (`REQ-F-005`, `REQ-F-006`):** Organized `Class -> Subject -> Materials` tree hierarchy with support for file attachments and external links.
- **500MB Upload Enforcement (`REQ-NF-001`, `ADD-003`, `BDD Scenario 3`):** Interactive file size selector with presets (1MB, 100MB, exact 500MB limit: 524,288,000 bytes, and 600MB overflow). Real-time display of RFC 7807 `413 Payload Too Large` error details.
- **Interactive Calendar View (`REQ-F-007`, `ADD-004`):** Aggregated visual deadline schedule with class-specific and global filtering, urgency tags, and material details.
- **Automated Reminders Center (`REQ-F-008`):** Unread notification counter in header, 7-day and 1-day deadline reminders, and one-click "Mark as Read" action.
- **Extension Requests Lifecycle (`REQ-F-009`, `REQ-F-010`, `ADD-006`, `BDD Scenario 2`):**
  - Students submit formal extension requests with medical/personal comments and requested deadlines.
  - Administrators review pending requests in a dedicated panel, approve with user or class-wide scope, and automatically shift the material deadline timestamp.
- **Material Deletion & Cascading Lifecycle (`REQ-F-011` / Addendum 02):** Administrators can permanently remove materials with automated cascading cleanup of calendar entries, active reminders, and pending requests.
- **Live System Audit Log Stream:** Real-time terminal view of `logs/system.log` displaying timestamped audit records for all operations and security events.
- **OpenAPI Contract Explorer:** Interactive visual breakdown of all 26 REST API operations.

---

## 5. Quick Start & Execution Commands

### 1. Launch Web Dashboard & REST API
```bash
# Option A: Root convenience script
python run.py

# Option B: Application module
python src/app.py
```
Then open your browser at **`http://127.0.0.1:5000/`**.

### 2. Run Full Test Suite (47 Tests, 100% Pass Rate)
Executes all unit, integration, Web UI endpoints, BDD scenarios (1–5), and contract checks:
```bash
python -m pytest tests/ -v
```

### 3. Run Automated OpenAPI Contract Validation
```bash
python scripts/validate_openapi.py
```

### 4. Inspect Live Audit Logs
```powershell
Get-Content logs/system.log -Tail 30
```

---

## 5. Verification vs. Validation Summary

- **Verification ("Are we building the system right?"):**
  - **OpenAPI 3.0.3 Conformance:** 26 operations, 34 schemas, 153 references verified via `scripts/validate_openapi.py`.
  - **Automated Test Suite:** 44/44 tests passing in 1.00s (`tests/test_server_api.py` and `tests/test_mock_api.py`).
  - **Storage Ceiling Limit:** Exact boundary test accepted 524,288,000 bytes (201 Created), rejected 629,145,600 bytes with HTTP 413 Payload Too Large.
  - **Standard Error Model:** 100% compliance with RFC 7807 problem details across all 4xx/5xx responses.
- **Validation ("Are we building the right system?"):**
  - Confirmed educator journey: class workspace setup, subject hierarchy, assignment publishing, calendar deadlines.
  - Confirmed student journey: invite joining, read-only access, viewing deadlines, extension requests.
  - Confirmed addendum intent: educators can delete obsolete materials, automatically eliminating dangling deadlines and orphaned requests.

---

## 6. Repository Artifacts & Governance Directory

```text
LabManager/
├── spec/                                 # Formal Requirements Baseline & Addenda
│   ├── project_description.md            # High-level charter and domain purpose
│   ├── srs.md                            # Formal SRS v1.0
│   ├── srs_addendum.md                   # Protocol and behavioral clarifications (Addendum 01)
│   ├── srs_addendum_02.md                # REQ-F-011: Material Deletion & Cascading (Addendum 02)
│   ├── openapi.yaml                      # OpenAPI 3.0.3 Contract (YAML)
│   └── openapi.json                      # OpenAPI 3.0.3 Contract (JSON, 26 operations)
│
├── docs/                                 # Project Engineering & Management Documentation
│   ├── api_design.md                     # REST architecture, URIs, schemas & RFC 7807 model
│   ├── features.md                       # Core system capabilities breakdown
│   ├── plan.md                           # Phased roadmap, duration modeling & Gantt schedule
│   ├── risks.md                          # Risk register & AI mitigation controls
│   ├── tickets.md                        # SDD work units (TICK-001 through TICK-026)
│   ├── traceability_matrix.md            # 100% bidirectional traceability mapping
│   ├── workflow.md                       # Ticket lifecycle & state machine
│   └── diagrams/                         # Architectural and process diagrams
│
├── logs/                                 # Gate Audits & Runtime Logging
│   ├── api_gate.md                       # API-GATE GO checkpoint record
│   ├── test_gate_base.md                 # TEST-GATE (Base implementation) GO record
│   ├── spec_addendum_gate.md             # SPEC-ADDENDUM-GATE (REQ-F-011) GO record
│   ├── test_gate_addendum.md             # TEST-GATE (Addendum implementation) GO record
│   ├── final_gate.md                     # FINAL-GATE project release GO record
│   └── system.log                        # Structured system audit trail
│
├── src/                                  # Component-Based Server Source Code
│   ├── core/                             # Logging, errors, security, response helpers
│   ├── models/                           # Domain dataclasses and schemas
│   ├── storage/                          # Thread-safe in-memory repository
│   ├── services/                         # Business logic services
│   ├── api/                              # REST Blueprint controllers
│   ├── templates/                        # Web UI HTML templates (SPA Dashboard)
│   ├── static/                           # Web UI static assets
│   └── app.py                            # Flask application factory
│
├── tests/                                # Automated TDD Test Suites
│   ├── test_server_api.py                # Server TDD test suite (23 tests: base + addendum)
│   ├── test_mock_api.py                  # Contract mock verification suite (21 tests)
│   └── test_web_ui.py                    # Web UI dashboard & docs test suite (3 tests)
│
├── scripts/                              # Tooling & Generation Scripts
│   ├── validate_openapi.py               # Automated OpenAPI validator
│   ├── mock_server.py                    # Contract mock runner
│   └── generate_report_docx.py           # Academic report generator
│
├── run.py                                # Convenience entrypoint to launch web app
├── Звіт_Лабораторна_робота_TDD_LabManager.docx  # Academic report (.docx)
└── README.md                             # Project overview and instructions
```

---

## 7. Key Stage-Gate Decisions

| Gate | Scope | Status | Audit Record |
| :--- | :--- | :---: | :--- |
| **API-GATE** | OpenAPI contract & mock verification | **APPROVED (GO)** | [`logs/api_gate.md`](logs/api_gate.md) |
| **TEST-GATE (Base)** | Causal independent test suite (RED phase) | **APPROVED (GO)** | [`logs/test_gate_base.md`](logs/test_gate_base.md) |
| **SPEC-ADDENDUM-GATE** | Specification addendum 02 (REQ-F-011) | **APPROVED (GO)** | [`logs/spec_addendum_gate.md`](logs/spec_addendum_gate.md) |
| **TEST-GATE (Addendum)** | Addendum causal test suite (RED phase) | **APPROVED (GO)** | [`logs/test_gate_addendum.md`](logs/test_gate_addendum.md) |
| **FINAL-GATE** | Final verification, human validation & release | **APPROVED (GO)** | [`logs/final_gate.md`](logs/final_gate.md) |
