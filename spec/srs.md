# Software Requirements Specification (SRS)
**Project Name:** LabManager
**Version:** 1.0

## 1. Introduction

### 1.1 Purpose
LabManager is an information system designed to organize and optimize the educational process. It serves as a centralized hub for tracking academic deadlines and structuring educational materials. 

### 1.2 System Boundaries
**In-Scope:**
- Manual creation of classes, subjects, materials, and deadlines.
- Custom class hierarchies managed by users.
- Built-in calendar for deadline tracking.
- Internal system reminders.
- Manual file uploads (images, text, archives, code files, links).

**Out-of-Scope:**
- Automated integration or data scraping from external LMS (e.g., Moodle, Google Classroom, MS Teams).
- Integration with external calendar applications (e.g., Google Calendar).

### 1.3 Domain Glossary
- **User:** A registered individual in the LabManager system.
- **Class:** A structural container created by a User to organize subjects, materials, and deadlines.
- **Administrator (Teacher):** A contextual role for a User who created a Class or was granted edit permissions. Administrators can manage content, users, and deadlines within that Class.
- **Student:** A contextual role for a User who joined a Class via an invite link but lacks edit permissions.
- **Subject:** A logical grouping within a Class representing a specific academic discipline.
- **Material:** An educational resource (file up to 500MB, or link) attached to a Subject.
- **Deadline:** A specific date and time associated with a Material or Assignment.
- **Extension Request:** A formal request with a comment, submitted by a Student to an Administrator, to change a Deadline.

---

## 2. Functional Requirements (FR)

### REQ-F-001: Unified User Registration
The system shall allow individuals to register for a single "User" account that acts dynamically as either an Administrator or Student based on context.
- **Acceptance Criteria:** A user can create an account using an email and password, log in, and access the main dashboard.

### REQ-F-002: Class Creation & Management
A User shall be able to create a new Class, automatically becoming its Administrator.
- **Acceptance Criteria:** A user clicks "Create Class", enters a name, and a new workspace is generated where they possess edit permissions.

### REQ-F-003: Joining a Class
The system shall allow an Administrator to generate an invite link. Users who click this link shall join the Class as "Students".
- **Acceptance Criteria:** A user clicks an invite link, is added to the Class roster, and can view (but not edit) the Class's contents.

### REQ-F-004: Role Assignment
An Administrator shall be able to grant Administrator rights to any other User within their Class.
- **Acceptance Criteria:** An Administrator selects a Student from the roster, clicks "Make Administrator", and the user gains edit permissions for that Class.

### REQ-F-005: Subject Management
Administrators shall be able to create Subjects within a Class to organize materials.
- **Acceptance Criteria:** An Administrator can add a new Subject to a Class, establishing a strict parent-child relationship (Class -> Subject).

### REQ-F-006: Material Upload
Administrators shall be able to upload Materials (images, text, archives, code files) or add external links to a specific Subject.
- **Acceptance Criteria:** A file uploaded is successfully attached to the chosen Subject, provided it does not exceed the 500MB size limit.

### REQ-F-007: Deadline Tracking (Calendar)
Administrators shall be able to assign Deadlines to Materials. All users in the Class shall be able to view these Deadlines on a built-in calendar.
- **Acceptance Criteria:** A set deadline accurately appears on the correct date in the Class's shared calendar view for all members.

### REQ-F-008: Automated Reminders
The system shall automatically generate internal reminders for all Class members 1 week and 1 day before an upcoming Deadline.
- **Acceptance Criteria:** A notification is displayed in the user's dashboard exactly 7 days and 1 day prior to the deadline timestamp.

### REQ-F-009: Extension Requests
Students shall be able to submit an Extension Request, including a comment, for a specific Deadline.
- **Acceptance Criteria:** A student clicks "Request Extension", inputs a reason, and the request appears in the Administrator's dashboard.

### REQ-F-010: Extension Approval
Administrators shall be able to approve or reject Extension Requests. Approving a request updates the deadline for the specified user or the entire Class.
- **Acceptance Criteria:** An Administrator clicks "Approve" on a request, and the system updates the deadline timestamp accordingly.

---

## 3. Non-Functional Requirements (NFR)

### REQ-NF-001: Storage Capacity
The system must support the uploading of individual files up to 500MB in size. Supported formats include images, text, archives, and code files.

### REQ-NF-002: Usability (Role Distinction)
The user interface must visually distinguish between Classes where the User is an "Administrator" and Classes where the User is a "Student", ensuring clear navigation and expectation of permissions.

---

## 4. Behavior-Driven Development (BDD) Scenarios

### Scenario 1: Joining a Class as a Student
**Given** a User is logged into the system
**And** an Administrator has generated an invite link for "Math 101"
**When** the User navigates to the invite link
**Then** the User is added to "Math 101" with the "Student" role
**And** the User can view materials but cannot upload new ones.

### Scenario 2: Requesting a Deadline Extension
**Given** a Student is viewing a Material with a set Deadline
**When** the Student clicks "Request Extension"
**And** the Student submits the request with the comment "I was sick"
**Then** an Extension Request is created
**And** the Administrator of the Class receives a notification of the request.

### Scenario 3: Uploading an Oversized File
**Given** an Administrator is adding Material to a Subject
**When** the Administrator attempts to upload a file sized 600MB
**Then** the system aborts the upload
**And** the system displays an error message stating "File exceeds the 500MB limit."
