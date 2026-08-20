# CourseHub v1 Implementation Epics and User Stories

**Status:** Ready for implementation planning
**Based on:** Approved PRD and approved architecture
**Date:** 2026-08-20

## Delivery strategy

Implement in vertical slices. Establish the backend contracts and persistence first, then connect the React learner journey, then build the admin workflow, and finally harden the system with tests and local setup documentation.

## Epic 1: Project foundation and local development

**Goal:** Create a reproducible React, Django, FastAPI, and MySQL development foundation without committing secrets.

### Story 1.1: Scaffold repository structure
As a developer, I want the frontend and backend directories created according to the approved architecture so that the project has clear ownership boundaries.

**Acceptance criteria**
- `frontend/` contains the React TypeScript application.
- `backend/` contains Django configuration, apps, FastAPI API package, and tests.
- Django and FastAPI are configured as separate processes.
- Shared configuration conventions are documented.

### Story 1.2: Configure environment-based settings
As a developer, I want database, JWT, CORS, and media settings loaded from environment variables so that secrets are not committed.

**Acceptance criteria**
- `.env.example` contains placeholder values only.
- MySQL settings support host, port, database, user, and password variables.
- JWT signing configuration is environment-based.
- No plaintext credential is committed to source control.

### Story 1.3: Establish local run workflow
As a beginner developer, I want clear commands for starting MySQL, Django, FastAPI, and React so that I can run CourseHub locally.

**Acceptance criteria**
- README documents prerequisites and startup order.
- README documents migrations, admin creation, media, ports, and troubleshooting.
- React proxies `/api` requests to FastAPI.
- A health endpoint confirms the API is running.

## Epic 2: Django domain model and persistence

**Goal:** Build the canonical MySQL-backed Django data layer with migrations and relational integrity.

### Story 2.1: Create custom user model
As a developer, I want a custom Django user model with email login and learner/admin roles so that authentication is secure and extensible.

**Acceptance criteria**
- Email is unique and is the login identifier.
- Role is restricted to `learner` or `admin`.
- Passwords use Django hashing.
- Public registration cannot assign the admin role.
- Initial migration works on a clean MySQL database.

### Story 2.2: Create catalog models
As an admin, I want categories, instructors, and courses stored as related entities so that catalog content is reusable and consistent.

**Acceptance criteria**
- Category name is unique.
- Course requires one category and one instructor.
- Course price is non-negative decimal.
- Course and instructor images are optional local media fields.
- Course timestamps and publication state are stored.

### Story 2.3: Create enrollment model and constraints
As a learner, I want my course enrollment persisted reliably so that My Learning remains accurate.

**Acceptance criteria**
- Enrollment references a learner and course.
- Database uniqueness prevents duplicate learner/course pairs.
- Foreign-key behavior preserves relational integrity.
- Migrations apply cleanly to MySQL.

### Story 2.4: Add Django admin and seed workflow
As a developer, I want Django admin and a small seed process so that I can create admin accounts and test catalog data locally.

**Acceptance criteria**
- Admin can create controlled administrator accounts.
- Catalog models are registered with useful list/search fields.
- Seed instructions do not expose secrets.
- Django admin is documented as a development shortcut only.

## Epic 3: Authentication and authorization API

**Goal:** Provide secure email-based JWT authentication and role enforcement through FastAPI.

### Story 3.1: Register learner accounts
As a visitor, I want to register with an email and password so that I can become a learner.

**Acceptance criteria**
- Valid data creates a learner account.
- Duplicate emails return field-level validation errors.
- Role input is ignored or rejected and never creates an admin.
- Passwords are never returned or logged.

### Story 3.2: Login, refresh, logout, and current user
As a learner or admin, I want a complete session lifecycle so that I can securely access the right features.

**Acceptance criteria**
- Login returns access token, refresh token, user identity, and role.
- Invalid credentials return a safe generic error.
- Refresh exchanges a valid refresh token for a usable access token.
- Logout clears or invalidates refresh state according to the selected JWT strategy.
- `/auth/me` returns the authenticated user.

### Story 3.3: Protect API dependencies
As a system owner, I want server-side role checks so that hidden UI controls cannot be bypassed.

**Acceptance criteria**
- Missing or invalid tokens return `401`.
- Learners calling admin endpoints receive `403`.
- Current user is derived from the token, never from client-supplied ownership fields.
- FastAPI and Django use compatible JWT signing configuration.

## Epic 4: Public course discovery and learner experience

**Goal:** Deliver the complete learner path from browsing to enrollment and My Learning.

### Story 4.1: Build public catalog API
As a learner, I want to retrieve courses with search and category filters so that I can find relevant learning.

**Acceptance criteria**
- Public course list returns card-ready fields.
- Search matches title and description.
- Category filtering works independently and with search.
- Pagination or bounded list behavior is documented.
- Errors use the consistent API envelope.

### Story 4.2: Build course details API
As a learner, I want course and instructor details so that I can evaluate a course before joining.

**Acceptance criteria**
- Detail response includes title, description, price, image, category, and instructor.
- Missing images return a safe null or fallback-compatible value.
- Enrollment state is included for an authenticated learner.
- Public unauthenticated detail remains available.

### Story 4.3: Build learner enrollment API
As a learner, I want to enroll for free with one action so that the course appears in My Learning.

**Acceptance criteria**
- Authenticated learners can enroll in published courses.
- Enrollment is atomic and idempotent.
- Repeated requests return enrolled state without a duplicate row.
- Ownership is derived from the authenticated user.

### Story 4.4: Build My Learning API
As a learner, I want to see only my enrolled courses so that I can track my learning.

**Acceptance criteria**
- Endpoint returns only the current learner's enrollments.
- Each item includes course summary and enrollment timestamp.
- Empty, loading, and API error states can be represented by the response contract.

### Story 4.5: Implement premium React learner UI
As a learner, I want an impressive royal-blue luxury interface so that discovering courses feels premium and clear.

**Acceptance criteria**
- React routes include catalog, course detail, login/register, and My Learning.
- Royal-blue and restrained gold token system is used consistently.
- Course cards show required summary information and accessible image alt text.
- Search, category filter, enrollment CTA, and protected navigation are functional.
- Responsive layout works at desktop and mobile widths.

## Epic 5: Admin catalog management

**Goal:** Give administrators a polished React dashboard for catalog CRUD and enrollment visibility.

### Story 5.1: Build admin catalog APIs
As an admin, I want protected CRUD APIs for courses, categories, and instructors so that I can maintain the catalog.

**Acceptance criteria**
- Admin-only list/create/update/delete routes exist for each resource.
- Course creation requires title, description, category, instructor, and price.
- Course image and instructor photo uploads are optional.
- Relationship validation prevents invalid category/instructor references.
- Learners receive `403` for every admin route.

### Story 5.2: Build course management UI
As an admin, I want to create, edit, and delete courses so that the catalog stays current.

**Acceptance criteria**
- Course table supports loading, error, empty, and success states.
- Create/edit form validates the required core fields.
- Image upload and replacement are supported.
- Delete requires confirmation.
- Success and error feedback is visible and accessible.

### Story 5.3: Build category and instructor management UI
As an admin, I want to manage reusable categories and instructor profiles so that course forms remain consistent.

**Acceptance criteria**
- Category CRUD is available from the admin dashboard.
- Instructor CRUD supports name, bio, and optional photo.
- Destructive actions require confirmation.
- Relationship errors explain why a category or instructor cannot be deleted.

### Story 5.4: Build course enrollment visibility
As an admin, I want to inspect enrolled learners by course so that I can understand catalog usage.

**Acceptance criteria**
- Admin can open a course enrollment view.
- Learner identity and enrollment timestamp are displayed.
- Endpoint and UI are admin-only.
- Empty enrollment state is clear.

## Epic 6: Frontend platform quality and accessibility

**Goal:** Make the React application maintainable, accessible, responsive, and resilient.

### Story 6.1: Create typed API client and server-state layer
As a developer, I want typed API calls and cache invalidation so that frontend behavior stays consistent.

**Acceptance criteria**
- API client centralizes base URL, headers, token behavior, and error parsing.
- Request and response types cover authentication, catalog, and enrollment flows.
- Enrollment and admin mutations invalidate affected queries.
- Duplicate requests during search/filter changes are avoided or controlled.

### Story 6.2: Implement protected routing and role-aware navigation
As a user, I want navigation to reflect my session and role so that I do not encounter confusing inaccessible screens.

**Acceptance criteria**
- Anonymous, learner, and admin route states are distinct.
- Unauthorized navigation redirects safely.
- UI hiding is paired with backend authorization.
- Logout clears client auth state and protected data.

### Story 6.3: Apply accessibility and responsive quality
As a user, I want the app to work with keyboard, assistive technology, and smaller screens.

**Acceptance criteria**
- Forms have labels and usable validation messages.
- Interactive controls have visible focus states.
- Images have meaningful alt text or are marked decorative appropriately.
- Main views are usable at mobile and desktop widths.
- Loading, error, empty, and success states are announced or clearly exposed.

## Epic 7: Verification, documentation, and release readiness

**Goal:** Prove the integrated local stack works and remains within v1 scope.

### Story 7.1: Add Django model and service tests
As a developer, I want automated backend tests for relationships and business rules so that regressions are caught early.

**Acceptance criteria**
- Tests cover custom user roles and email uniqueness.
- Tests cover catalog relationships and price validation.
- Tests cover unique, atomic, idempotent enrollment.
- Tests cover admin service authorization.

### Story 7.2: Add FastAPI contract and authorization tests
As a developer, I want API tests for status codes and error envelopes so that the React client has stable behavior.

**Acceptance criteria**
- Tests cover register, login, refresh, logout, and `/auth/me`.
- Tests cover public catalog search/filter and detail.
- Tests cover learner enrollment/My Learning ownership.
- Tests cover admin-only endpoints and consistent `401`/`403` responses.

### Story 7.3: Add React flow tests and smoke path
As a developer, I want frontend tests and one end-to-end smoke path so that the main learner journey is verified.

**Acceptance criteria**
- Tests cover registration, login, protected routing, search/filter, enrollment, and My Learning.
- Admin CRUD feedback and destructive confirmations are covered.
- Smoke path passes: register learner → login → browse → enroll → My Learning.

### Story 7.4: Complete beginner-friendly documentation
As a beginner developer, I want setup and troubleshooting documentation so that I can operate the project without assistance.

**Acceptance criteria**
- README covers MySQL database creation, environment variables, migrations, admin creation, media, and startup commands.
- README explicitly says supplied credentials are local-only and must not be committed.
- README documents separate Django and FastAPI ports.
- README lists common errors and recovery steps.

## Dependency order

1. Epic 1 foundation
2. Epic 2 Django persistence
3. Epic 3 authentication and authorization
4. Epic 4 learner vertical slice
5. Epic 5 admin vertical slice
6. Epic 6 frontend quality hardening
7. Epic 7 verification and release readiness

## Scope guardrails

Do not add payments, cloud storage, reviews, ratings, wishlists, video delivery, analytics, instructor self-service, or deployment work to these v1 stories unless a new approved scope decision is recorded.

## Definition of ready for implementation

The implementation backlog is ready when each story is implemented against the approved PRD and architecture, acceptance criteria are testable, and credentials remain environment-only.

**Status:** Approved for implementation

**Approval record:** Approved by user on 2026-08-20. Epic 1 project foundation is now in progress.
