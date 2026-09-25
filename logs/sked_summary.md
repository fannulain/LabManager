# SKED Dialogue Summary

## Date of Dialogue
2026-09-25

## Participants
- **User:** Product Owner / Domain Expert
- **AI (Antigravity):** Requirements Elicitor / Systems Analyst

## Objectives
Elicit requirements, clarify system boundaries, and establish a shared understanding for the "LabManager" information system.

## Identified Uncertainties & Resolutions
1. **Uncertainty:** What are the specific user roles, and do students have administrative capabilities?
   - **User Decision:** Adopted a contextual role model. All accounts are generic "Users". A User becomes an "Administrator (Teacher)" of a Class if they create it or are granted edit permissions. A User is a "Student" if they join via an invite link.
2. **Uncertainty:** How will data populate the system, and should there be integrations with external LMS (Moodle, Google Classroom)?
   - **User Decision:** Explicitly excluded automated integrations for the current version to maintain a manageable scope. All data entry (deadlines, materials) will be manual.
3. **Uncertainty:** How should the class hierarchy be structured?
   - **User Decision:** Students/Users have the freedom to create their own class hierarchy (e.g., Year -> Tab -> Course). The only strict system-enforced hierarchy is that Materials and Labs must be linked to a specific Subject.
4. **Uncertainty:** How are deadline extensions handled in student-created "local classes"?
   - **User Decision:** Extension requests remain a valuable feature even in local classes. Students can use the extension request feature (with comments) to notify the local Administrator (the student who created the class) that a professor has changed a deadline.

## Corrected AI Assumptions
- **Assumption:** The AI initially assumed distinct registration paths for "Teachers" and "Students".
  - **Correction:** The user corrected this to a unified "User" role with contextual permissions based on class creation/invitation.
- **Assumption:** The AI suggested possible external LMS integrations.
  - **Correction:** The user explicitly placed this outside the system boundaries for the initial release.

## SPEC-GATE Decision
- **Status:** APPROVED. 
- The Domain Glossary, System Boundaries, and Core Requirements were reviewed and confirmed by the user without contradictions.
