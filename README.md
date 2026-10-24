# LabManager (Educational Materials and Laboratory Manager)

An information system designed to organize and optimize the educational process by serving as a centralized hub for tracking academic deadlines and structuring educational materials.

Developed using **Specification-Driven Development (SDD)** with a strict **Human-in-the-Loop** AI-augmented engineering pipeline.

---

## 1. Core System Capabilities

- **Unified User Model & Contextual Roles:** Generic user accounts that dynamically function as an **Administrator** (educator/creator with content edit rights) or **Student** (read-only member joined via invite link) depending on class context (`REQ-F-001`, `REQ-F-002`, `REQ-F-003`, `REQ-F-004`).
- **Academic Material Structuring:** Strict hierarchical organization (`Class -> Subject -> Materials`) supporting files up to 500MB (images, text, archives, code) and external links (`REQ-F-005`, `REQ-F-006`, `REQ-NF-001`).
- **Deadline Tracking & Calendar:** Built-in interactive calendar displaying assignment deadlines for all class members (`REQ-F-007`).
- **Automated Reminders:** Internal notification triggers dispatched exactly 7 days and 1 day prior to upcoming deadlines (`REQ-F-008`).
- **Deadline Extension Requests:** Formal workflow enabling students to submit extension requests with comments, which administrators can review, approve, or reject (`REQ-F-009`, `REQ-F-010`).
- **Visual Role Distinction:** Dynamic UI themes and badges immediately separating administrative workspaces from student view-only classes (`REQ-NF-002`).

---

## 2. SDD Engineering Methodology & Roles

The project strictly follows the **Specification-Driven Development (SDD)** paradigm, maintaining an immutable requirements contract and formal stage-gates before code transitions:

- **Human Reviewer:** Product Owner, Lead Architect, and Quality Auditor. Retains exclusive, non-delegable authority over Stage-Gate decisions (`SPEC-GATE`, `PLAN-GATE`, `API-GATE`, `STAGE-GATE`), user intent validation, and requirements baseline approvals.
- **AI Coding Agent (Antigravity):** Autonomous technical partner responsible for initial decomposition, automated test suite generation, feature implementation adhering strictly to SRS boundaries, CI verification, and documentation drafting.

---

## 3. REST API Specification & Mock API (Lab #4)

In accordance with API-First design, formal contracts and mocks are established prior to server implementation:

- **OpenAPI 3.0.3 Specification:** [`spec/openapi.yaml`](spec/openapi.yaml) and [`spec/openapi.json`](spec/openapi.json)
- **REST Architecture & Resource Model:** [`docs/api_design.md`](docs/api_design.md)
- **SRS Behavioral Addendum:** [`spec/srs_addendum.md`](spec/srs_addendum.md)
- **API-GATE Decision Record:** [`logs/api_gate.md`](logs/api_gate.md)

### Running Automated Specification Validation
```bash
python scripts/validate_openapi.py
```

### Running the Contract Mock API Server
```bash
# Option A: Built-in OpenAPI specification runner
python scripts/mock_server.py

# Option B: Stoplight Prism CLI (if installed)
npx @stoplight/prism-cli mock spec/openapi.yaml -p 8000
```

### Running the Mock Contract Test Suite (21 Scenarios)
```bash
python -m pytest tests/test_mock_api.py -v
```

---

## 4. Repository Structure

```text
LabManager/
├── spec/                        # Formal Requirements Baseline (Immutable Contract)
│   ├── project_description.md   # High-level project charter and domain purpose
│   ├── srs.md                   # Formal Software Requirements Specification (v1.0)
│   ├── srs_addendum.md          # Architectural addendum & protocol refinements
│   ├── openapi.yaml             # OpenAPI 3.0.3 REST Contract (YAML)
│   └── openapi.json             # OpenAPI 3.0.3 REST Contract (JSON)
│
├── docs/                        # Project Engineering & Management Artifacts
│   ├── features.md              # Detailed breakdown of core system features
│   ├── api_design.md            # REST resource decomposition, URIs, schemas & RFC 7807 model
│   ├── workflow.md              # SDD issue tracking setup, statuses, and role-based lifecycle diagram
│   ├── tickets.md               # 24 decomposed work units (Tests, Features, Gates, Docs)
│   ├── plan.md                  # Implementation phases, critical path analysis, and Gantt schedule
│   ├── risks.md                 # Risk register (Classical tech risks & AI pipeline-specific controls)
│   ├── traceability_matrix.md   # Bidirectional mapping from SRS IDs to tickets, API operations, code, and tests
│   └── task_lifecycle_diagram.svg # Standalone SVG state diagram for the ticket lifecycle
│
├── scripts/                     # Automation, validation and mock runners
│   ├── validate_openapi.py      # Automated OpenAPI syntax and structural validator
│   └── mock_server.py           # Specification-driven mock API server
│
├── logs/                        # Governance, Audit Records & Decision Checkpoints
│   ├── agent_info.md            # AI Coding Agent profile, operational scope, and tool access
│   ├── conflicts.md             # Merge conflict and resolution audit log
│   ├── sked_summary.md          # SKED dialogue summary and SPEC-GATE approval record
│   ├── plan_gate.md             # Formal PLAN-GATE audit checklist and GO decision record
│   └── api_gate.md              # Formal API-GATE audit checklist and GO decision record
│
├── src/                         # Application source code (Backend & Frontend)
└── tests/                       # Automated test suites
    └── test_mock_api.py         # Mock API positive & negative scenario suite (21 tests)
```

---

## 5. Key Project References

- **Requirements Baseline:** [`spec/srs.md`](spec/srs.md)
- **SRS Addendum:** [`spec/srs_addendum.md`](spec/srs_addendum.md)
- **REST API Design Document:** [`docs/api_design.md`](docs/api_design.md)
- **Work Process & State Machine:** [`docs/workflow.md`](docs/workflow.md)
- **Decomposed Tickets:** [`docs/tickets.md`](docs/tickets.md)
- **Traceability Matrix:** [`docs/traceability_matrix.md`](docs/traceability_matrix.md)
- **Project Schedule & Gantt:** [`docs/plan.md`](docs/plan.md)
- **Risk Register:** [`docs/risks.md`](docs/risks.md)
- **PLAN-GATE Decision Audit:** [`logs/plan_gate.md`](logs/plan_gate.md)
- **API-GATE Decision Audit:** [`logs/api_gate.md`](logs/api_gate.md)
