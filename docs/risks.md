# Risk Register and AI-Augmented Pipeline Controls

**Project:** LabManager  
**Methodology:** Specification-Driven Development (SDD)  
**Roles:** Human Reviewer, AI Coding Agent  

---

## 1. Risk Register (Classical & AI-Specific Risks)

| Risk ID | Category | Risk Description & Manifestation | Potential Impact | Detection Method | Prevention & Mitigation Strategy | Criticality |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **RSK-01** | Classical (Tech) | **Large File Upload Exhaustion:** Uploading 500MB files consumes server memory or crashes HTTP pipeline (`REQ-NF-001`). | High: Server crash, Denial of Service, poor user experience. | Load/stress testing with chunks up to 500MB; memory profiling. | Stream-based multipart uploads directly to disk or object store; reject files >500MB at gateway level before buffering in RAM. | **High** |
| **RSK-02** | Classical (Req) | **Role Escalation Vulnerability:** Faulty permission logic in Class invitation or role change allows Student to act as Admin (`REQ-F-004`). | Critical: Unauthorized modification/deletion of classes, materials, deadlines. | Automated unit/integration test suites for authorization bypass; security peer review. | Strict backend contextual role enforcement on all API endpoints; test suite asserts read-only bounds. | **Critical** |
| **RSK-03** | AI-Specific | **Requirement Misinterpretation & Scope Creep:** Agent generates LMS integrations (Moodle/Google Classroom) or Google Calendar syncs explicitly excluded in SRS 1.2. | Medium/High: Bloated codebase, architectural divergence, missed deadlines. | Human review of decomposition against SRS boundaries; diff inspection during PR. | Explicit system boundaries provided in agent prompts; human gate rejection (REVISE) for out-of-scope code. | **Medium** |
| **RSK-04** | AI-Specific | **Error Correlation Between Code & Tests:** Agent writes a flawed implementation and crafts matching flawed unit tests, causing false-positive CI passes. | High: Undetected defects reach validation phase; broken functionality in production. | Human Reviewer code review focusing on test assertions; independent BDD verification. | Human Reviewer inspects test oracle logic; enforce strict adherence to given BDD scenarios; separate test prompt context if needed. | **High** |
| **RSK-05** | AI-Specific | **Context Loss / Degradation:** In long conversational sessions or complex refactors, agent forgets key constraints (e.g. single User model with contextual roles). | Medium: Agent re-introduces deprecated multi-account schema or invalid foreign keys. | Automated linting; TypeScript/Pydantic schema validation; human code review. | Maintain single-source-of-truth specification files (`spec/srs.md`); compact context frequently; provide requirements IDs in PR descriptions. | **Medium** |
| **RSK-06** | AI-Specific | **Non-Determinism in Code Generation:** Successive agent prompts produce incompatible code styles, mismatched variable naming, or regressions. | Medium: Merge conflicts, code smell, brittle integration points. | Strict static analysis (flake8/black/eslint), pre-commit hooks, CI regression test suite. | Pin linters, formatters, and coding conventions in repository rules; enforce clean branch isolation. | **Medium** |
| **RSK-07** | AI-Specific | **Tool Calling & File Manipulation Glitches:** Agent inadvertently overwrites unaffected files or corrupts project configuration during batch edits. | High: Loss of working code, broken builds, wasted debugging time. | Git diff audit before staging/committing; automated build check. | Atomic commits; mandatory verification step (`TICK-021`); prompt verification before destructive commands. | **Low** |
| **RSK-08** | AI-Specific | **Superficial Human Oversight ("Rubber-Stamping"):** Human Reviewer approves PRs without deep scrutiny due to high AI output velocity. | Critical: Technical debt accumulates, silent logical bugs escape to production. | Mandatory checklist for Gate approvals; requirement for explicit test evidence before merge. | Stage-Gates cannot be marked `GO` without reproducible test execution logs and manual verification notes. | **Critical** |

---

## 2. High-Impact Requirements Requiring Strengthened Controls

Certain requirements carry an elevated cost of failure and are subject to mandatory extra verification and human inspection checkpoints:

1. **REQ-NF-001 (500MB File Size Handling):**
   - *Cost of Failure:* Memory starvation, denial of service, data corruption.
   - *Control Measure:* Dedicated negative testing suite (`TICK-011`) validating exact byte limits, streaming upload benchmarks, and explicit error response validation.

2. **REQ-F-004 & REQ-F-003 (Contextual Role Elevation & Access Control):**
   - *Cost of Failure:* Privilege escalation across Class workspaces.
   - *Control Measure:* Comprehensive authorization test matrix; mandatory Human Reviewer code sign-off for permission middleware before merging `TICK-006`.

3. **REQ-F-008 & REQ-F-010 (Deadline Shifting & Automated Reminders):**
   - *Cost of Failure:* Students miss critical assignment deadlines or receive incorrect overdue notices.
   - *Control Measure:* Time-mocked unit testing (7 days and 1 day boundaries) and regression tests on timestamp recalculations upon extension approval.
