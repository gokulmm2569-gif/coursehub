# CourseHub v1 Product Requirements Document

**Status:** Approved  
**Created:** 2026-08-19  
**Author:** Gokul  
**Source:** Approved CourseHub product brief

## 1. Product definition

CourseHub is a local-first learning catalog and enrollment application for a portfolio project. Registered learners discover courses through a searchable, category-filtered catalog, view course details, enroll for free, and manage enrolled courses in My Learning. Administrators manage the catalog and enrollment visibility through a React dashboard.

## 2. Goals and measurable outcomes

1. A learner can complete registration, login, course discovery, enrollment, and My Learning without administrator assistance.
2. An administrator can manage categories, reusable instructor profiles, courses, local images, and course enrollments from the React dashboard.
3. The API protects authenticated and admin-only operations with JWT and role-based permissions.
4. A beginner can run the full stack locally using the README and MySQL setup instructions.

## 3. Personas

### Learner
A registered demo user who wants to discover relevant courses and keep track of courses they joined. Learners can access learner-facing features only.

### Administrator
A trusted catalog manager whose account is created separately by a developer or through Django admin. Administrators maintain catalog data and inspect enrollments; they do not self-select the admin role during public registration.

### Builder/developer
The project owner who uses the application to learn React, Django/DRF, MySQL, JWT, RBAC, relational modeling, and local file uploads.

## 4. Functional requirements

### FR-1 Authentication and roles
- The system shall allow a new public account to register with learner privileges.
- The system shall allow learners and administrators to log in.
- The system shall issue JWT access and refresh tokens.
- The system shall refresh an expired access token using a valid refresh token.
- Public registration shall never allow a requester to choose or escalate to the admin role.
- Admin accounts shall be created separately by a developer or through Django admin.
- The API shall reject unauthenticated requests to protected operations.
- The API shall reject learner requests to admin-only operations.
- The UI shall show only actions available to the authenticated role.
- Logout shall clear the client authentication state.

### FR-2 Course catalog discovery
- The learner catalog shall display available courses in a responsive card grid.
- Each course card shall show the course image when available, title, category, instructor, and display price.
- Learners shall search courses by matching text in title or description.
- Learners shall filter courses by category.
- Search and category filtering shall be combinable.
- The catalog shall provide clear empty states when no courses match.
- The catalog shall provide loading and error states.

### FR-3 Course details
- Learners shall open a dedicated course detail view.
- The detail view shall show image, title, full description, display price, category, and instructor information.
- The detail view shall show the enrollment state for the current learner.
- A logged-in learner shall be able to enroll with one action.
- Enrollment shall be free; no payment or checkout flow shall be shown.
- If the learner is already enrolled, repeating the enrollment action shall keep the learner enrolled and communicate that state without creating a duplicate enrollment.
- Unauthenticated users attempting to enroll shall be directed to authenticate.

### FR-4 My Learning
- An authenticated learner shall have a My Learning view.
- My Learning shall list the learner's enrolled courses.
- Each item shall provide enough information to identify the course and open its details.
- My Learning shall provide loading, error, and empty states.
- A learner shall not see another learner's enrollments.

### FR-5 Admin dashboard
- An administrator shall have access to a dedicated React admin dashboard.
- The dashboard shall provide course list, create, edit, and delete operations.
- Course creation shall require title, description, category, instructor, and price; course image shall be optional.
- The dashboard shall provide category list, create, edit, and delete operations subject to relationship validation.
- The dashboard shall provide reusable instructor profile list, create, edit, and delete operations.
- Instructor profiles shall support name, bio, and optional photo.
- Course forms shall select one existing category and one existing instructor.
- Course forms shall support upload/update of a local course image.
- Instructor forms shall support upload/update of a local instructor photo.
- The dashboard shall show enrolled learners for each course.
- Admin operations shall provide confirmation for destructive actions and visible success/error feedback.
- Django `/admin` may remain available as a development/testing shortcut but shall not be the primary admin workflow.

### FR-6 Data and media behavior
- Each course shall belong to exactly one category.
- Each course shall reference exactly one reusable instructor profile.
- Enrollment shall relate a learner to a course and enforce one enrollment per learner/course pair.
- Course prices shall be stored and displayed but shall not trigger payment logic.
- Uploaded images shall be stored through Django local media storage under `MEDIA_ROOT`.
- Missing images shall use an accessible non-broken fallback presentation.

## 5. User stories and acceptance criteria

### US-1 Register as a learner
**As a visitor, I want to create a learner account so that I can enroll in courses.**

Acceptance criteria:
- Given valid registration data, when I submit the form, then a learner account is created and I receive clear success feedback.
- Given an already-used email/username, when I submit registration, then the request is rejected with an actionable validation message.
- Given an attempted admin role field or privilege escalation, when registration is submitted, then the account remains a learner or the request is rejected.
- Given invalid or incomplete data, when I submit, then field-level errors are shown.

### US-2 Log in securely
**As a learner or admin, I want to log in so that I can use role-appropriate features.**

Acceptance criteria:
- Valid credentials return usable access and refresh tokens.
- Invalid credentials do not reveal whether the account or password was incorrect beyond a general error.
- A learner is routed to the learner experience; an admin is routed to the admin dashboard.
- Expired access tokens can be refreshed when the refresh token is valid.

### US-3 Discover courses
**As a learner, I want to search and filter the catalog so that I can find relevant courses.**

Acceptance criteria:
- The catalog shows course cards with required summary information.
- Search matches title and description without matching instructor name as a v1 requirement.
- Category filtering updates the displayed results.
- Search and category filtering together return only courses satisfying both criteria.
- No-match results show a clear empty state.

### US-4 Inspect course details
**As a learner, I want to view course details so that I can decide whether to enroll.**

Acceptance criteria:
- The detail view displays all required course, category, and instructor information.
- The displayed price is visible but no payment control is present.
- The current enrollment state is visible.

### US-5 Enroll for free
**As a learner, I want to enroll in a course with one action so that it appears in My Learning.**

Acceptance criteria:
- An authenticated learner can enroll successfully without payment.
- The enrollment state updates after success.
- Repeating enrollment is idempotent: the learner stays enrolled and no duplicate record is created.
- A learner cannot enroll another user or alter enrollment ownership.

### US-6 View My Learning
**As a learner, I want to see my enrolled courses so that I can track my learning.**

Acceptance criteria:
- Only the authenticated learner's enrollments are returned.
- Enrolled courses are listed with links to details.
- An empty list explains that no courses have been joined yet.

### US-7 Manage catalog as admin
**As an admin, I want to manage courses, categories, instructors, and images so that the catalog stays current.**

Acceptance criteria:
- Admin CRUD controls are available in the React dashboard.
- Course creation requires title, description, category, instructor, and price.
- Course image is optional and can be added or replaced.
- Instructor photo is optional and can be added or replaced.
- Courses use one category and one reusable instructor.
- Delete actions require confirmation and show the resulting status.
- Learners receive authorization errors if they call admin endpoints directly.

### US-8 Inspect enrollments as admin
**As an admin, I want to see enrolled learners per course so that I can understand catalog usage.**

Acceptance criteria:
- An admin can open a course's enrollment view.
- The view identifies enrolled learners and relevant enrollment records.
- Learners cannot access this view or endpoint.

## 6. Non-functional requirements

### Security
- Use JWT access/refresh authentication via `djangorestframework-simplejwt`.
- Enforce authorization server-side; UI hiding is not a security boundary.
- Hash passwords using Django's secure password mechanisms.
- Validate uploaded file types and sizes appropriate for local development.
- Validate and sanitize user-controlled text and use parameterized ORM queries.
- Protect enrollment creation so ownership comes from the authenticated user.

### Usability and accessibility
- Use semantic controls, labels, keyboard-accessible navigation, and visible focus states.
- Provide readable validation, loading, error, success, and empty states.
- Provide meaningful alternative text for course and instructor images.
- Make learner and admin experiences usable on desktop and smaller screens.

### Performance
- Avoid loading unnecessary full datasets when list endpoints can support filtering/search.
- Keep image dimensions and upload sizes reasonable for local development.
- Avoid duplicate API requests during catalog search/filter interactions.

### Reliability and maintainability
- Use clear API error responses and consistent frontend handling.
- Preserve relational integrity for category, instructor, and enrollment relationships.
- Keep configuration environment-based for database and local development settings.
- Document setup, migrations, media handling, test users, and common troubleshooting in README.

## 7. API-level requirement outline

The implementation should expose REST resources for authentication, courses, categories, instructors, and enrollments. Exact URL naming may be finalized during architecture, but the API must support public/read operations for catalog discovery, authenticated learner operations for enrollment and My Learning, and admin-protected CRUD/enrollment operations. Authentication errors should use standard HTTP semantics, and duplicate enrollment should be handled idempotently.

## 8. Scope guardrails

Do not add payments, deployment, cloud storage, instructor-name search, multiple categories, reviews, ratings, wishlists, video delivery, analytics, or instructor self-service in v1. Django admin remains a development shortcut, not a replacement for the React admin dashboard.

## 9. Definition of done

CourseHub v1 is ready for architecture and implementation when:

- The learner stories and admin stories above pass end-to-end locally.
- API authorization prevents learner access to admin operations.
- Duplicate enrollment is prevented and handled idempotently.
- Course creation enforces the agreed core required fields.
- MySQL persistence, local media uploads, and migrations work from a clean setup.
- README instructions allow a beginner to start frontend, backend, and database locally.
- No out-of-scope v2 feature is required for acceptance.

## 10. Next BMAD workflow

Review this PRD, then continue with `bmad-architecture` and/or `bmad-ux` before creating implementation epics and stories. No application code should be written until the requirements and technical/UI direction are approved.

**Status:** Approved

---

## Decision log

- Duplicate enrollment is idempotent: keep the learner enrolled and do not create a duplicate record.
- Course creation requires title, description, category, instructor, and price; image is optional.
- Public registration creates learner accounts only; admins are created separately by a developer or through Django admin.
- No coding yet; the user is a beginner and wants a step-by-step BMAD workflow.

---

## Review questions

1. Does this PRD accurately represent the approved v1 scope?
2. Are the acceptance criteria clear enough to guide implementation?
3. Should the next workflow be architecture first, UX first, or both in sequence?
4. Are there any API, validation, or README expectations to add before approval?

---

## Revision history

- 2026-08-19: Initial PRD drafted from approved product brief and discovery decisions.
- 2026-08-19: Added idempotent duplicate enrollment, core course required fields, and separate admin creation decisions.
- 2026-08-19: Added complete user stories, acceptance criteria, non-functional requirements, API outline, scope guardrails, and definition of done.

---

## Traceability note

Every requirement in this PRD traces to the approved CourseHub brief or to explicit discovery decisions. Payment, deployment, cloud media, and other deferred capabilities are intentionally excluded from the v1 acceptance boundary.

---

## Approval

**Approved by user on 2026-08-19.**

This document is now the baseline for the architecture/UX workflow and subsequent epics and stories.

---

## Beginner guidance

This PRD describes what CourseHub must do, not how to code it. The next step is to choose the system structure and screen patterns; implementation should come only after that direction is reviewed.

---

## Glossary

- **Learner:** A public self-registered user who can browse and enroll.
- **Admin:** A separately created privileged user who manages catalog data.
- **Enrollment:** A unique learner/course relationship.
- **Display price:** A stored course price shown for realism but not charged in v1.
- **Local media:** Files served from Django's local `MEDIA_ROOT` during development.

---

## Final review summary

CourseHub v1 is intentionally small but complete: one learner experience, one admin experience, one relational backend, and no payment or deployment complexity. The requirements prioritize secure role boundaries, a reliable enrollment model, practical CRUD, and beginner-friendly local setup.

---

## Workflow state

- Product brief: approved
- PRD: approved by user on 2026-08-19
- Architecture: ready to start
- UX: not started
- Epics/stories: not started
- Implementation: not started

---

## Change control

Any request to add deferred features to v1 should be reviewed against the scope guardrails and recorded as a separate decision before implementation.

---

## End of PRD
