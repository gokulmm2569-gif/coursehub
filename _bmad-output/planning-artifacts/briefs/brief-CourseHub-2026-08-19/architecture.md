# CourseHub v1 Technical Architecture

**Status:** Approved  
**Date:** 2026-08-19  
**Based on:** Approved CourseHub PRD

## 1. Architecture decision

CourseHub will use a three-part local development stack:

- **Frontend:** React with TypeScript, Vite, React Router, and a small API client layer.
- **Core backend:** Django with Django REST Framework, Django ORM, Django authentication, Django admin, and Simple JWT.
- **API boundary:** FastAPI as a versioned API facade for learner/admin application traffic.
- **Database:** MySQL using environment-based connection settings. The supplied local defaults are `root` and `admin1230`; these must be stored in environment variables and never committed to source control.

Django remains the source of truth for models, migrations, relational integrity, media storage, and privileged catalog administration. FastAPI owns the public application API contract and delegates persistence/business operations to Django services rather than introducing a second ORM or second set of models.

## 2. Why this split

This keeps the requested technologies while avoiding two competing data layers:

- Django provides mature relational modeling, migrations, admin, authentication primitives, and local media handling.
- FastAPI provides an explicit, typed, OpenAPI-friendly API surface for the React client.
- A shared `backend/core` service layer prevents business rules from being duplicated between FastAPI routes and Django admin/DRF code.
- MySQL remains the only persistent store.

Trade-off: running two Python web processes is more operationally complex than Django-only DRF. For a beginner project, that complexity is contained by keeping FastAPI thin and documenting one-command local startup later.

## 3. Repository shape

```text
coursehub/
  frontend/
    src/
      app/                 # routing, providers, app shell
      features/
        auth/
        courses/
        enrollments/
        admin/
      components/
      lib/api/              # typed fetch client and token handling
      types/
    public/
  backend/
    manage.py
    config/
      settings/
      urls.py
      asgi.py
    apps/
      accounts/
      catalog/
      enrollments/
    api/
      main.py              # FastAPI app
      routers/
        auth.py
        courses.py
        categories.py
        instructors.py
        enrollments.py
      dependencies.py
      schemas/
    services/
      auth.py
      catalog.py
      enrollment.py
    tests/
  .env.example
  README.md
```

## 4. Runtime boundaries

### React

- Calls FastAPI only through `/api/v1`.
- Stores access token in memory where practical; stores refresh token in a secure strategy documented during implementation.
- Never decides authorization; it only adapts the interface to the role returned by the backend.
- Uses typed request/response models generated or maintained from the FastAPI OpenAPI schema.

### FastAPI

- Handles request validation, response serialization, API versioning, authentication dependency wiring, and HTTP semantics.
- Verifies JWT access tokens and resolves the current Django user.
- Applies learner/admin authorization dependencies.
- Calls shared service functions for all writes and relationship-sensitive reads.
- Does not create independent SQLAlchemy models or migrations.

### Django

- Owns Django models, migrations, admin, password hashing, media configuration, and database transactions.
- Owns the canonical user, category, instructor, course, and enrollment entities.
- Exposes internal service functions that FastAPI calls in-process.
- May retain Django admin at `/django-admin/` for developer-created admin accounts and debugging.

## 5. Data model

### User

Use Django's custom user model from the beginning, with email as the login identifier if practical. Required concepts:

- `id`
- `email` unique
- `password` hashed by Django
- `first_name`, `last_name`
- `role`: `learner` or `admin`
- `is_active`, timestamps

Public registration always sets `role=learner`. Admin accounts are created through Django admin or a controlled developer command.

### Category

- `id`
- `name` unique
- `description` optional
- timestamps

### Instructor

- `id`
- `name`
- `bio`
- `photo` nullable local media field
- timestamps

### Course

- `id`
- `title`
- `description`
- `category_id` required foreign key
- `instructor_id` required foreign key
- `price` decimal, non-negative
- `image` nullable local media field
- `is_published` boolean, default true for v1 unless the UI needs draft state
- timestamps

### Enrollment

- `id`
- `learner_id` foreign key to User
- `course_id` foreign key to Course
- `created_at`
- unique constraint on `(learner_id, course_id)`

Enrollment creation must use an atomic transaction and `get_or_create` or equivalent conflict-safe behavior. Duplicate enrollment returns the existing enrollment state rather than creating a second row.

## 6. API contract

Base path: `/api/v1`

### Authentication

- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/token/refresh`
- `POST /auth/logout`
- `GET /auth/me`

Registration accepts learner profile fields only. Login returns an access token, refresh token, user identity, and role. Logout invalidates/blacklists refresh tokens if token rotation/blacklisting is enabled.

### Catalog

- `GET /courses?search=&category_id=&page=` — public list
- `GET /courses/{course_id}` — public detail
- `GET /categories` — public list
- `GET /instructors/{instructor_id}` — public detail

### Learner

- `POST /courses/{course_id}/enroll` — learner only, idempotent
- `GET /me/enrollments` — learner only
- `GET /me/enrollments/{enrollment_id}` — learner ownership required

### Admin

- `GET|POST /admin/courses`
- `GET|PATCH|DELETE /admin/courses/{course_id}`
- `GET|POST /admin/categories`
- `GET|PATCH|DELETE /admin/categories/{category_id}`
- `GET|POST /admin/instructors`
- `GET|PATCH|DELETE /admin/instructors/{instructor_id}`
- `GET /admin/courses/{course_id}/enrollments`

Admin create/update endpoints accept multipart form data when an image is uploaded. JSON is used when no file is included, or the implementation may standardize all admin writes on multipart.

### Error shape

Use a consistent envelope:

```json
{
  "error": {
    "code": "validation_error",
    "message": "One or more fields are invalid.",
    "fields": {"title": ["This field is required."]}
  }
}
```

Use `401` for missing/invalid authentication, `403` for insufficient role, `404` for missing resources, `409` for relationship conflicts where idempotency does not apply, and `422` for request validation where appropriate.

## 7. Authentication and authorization

- Use `djangorestframework-simplejwt` token semantics, with FastAPI verifying the same signing configuration and claims.
- Keep signing secret and token lifetimes in environment configuration.
- Add a FastAPI dependency for `current_user` and a second dependency for `require_admin`.
- Never accept `user_id` from the client for learner-owned operations; derive ownership from the JWT subject.
- Enforce role checks in FastAPI and again in service functions for defense in depth.
- Configure CORS only for the local React origin during development.
- Use secure password hashing through Django; never store or log plaintext passwords.

## 8. Media and database configuration

Environment variables:

```env
DJANGO_SECRET_KEY=replace-me
DEBUG=true
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=coursehub
MYSQL_USER=root
MYSQL_PASSWORD=admin1230
JWT_SIGNING_KEY=replace-me
FRONTEND_ORIGIN=http://localhost:5173
MEDIA_ROOT=media
```

The credentials above are local-development defaults only. The repository must include `.env.example`, not a populated `.env`. Use Django `MEDIA_ROOT`/`MEDIA_URL` for local files and serve media only in development through Django URL configuration.

## 9. Service layer rules

The service layer is the architectural invariant:

- `catalog_service`: course/category/instructor CRUD and relationship validation.
- `enrollment_service`: atomic idempotent enrollment and learner-owned queries.
- `auth_service`: registration role enforcement and token-related user operations.

FastAPI routers should be thin: parse input, call service, map result to schema. Django admin actions should call the same services for rules that matter, especially relationship validation and enrollment behavior.

## 10. Frontend structure

Use feature-oriented React modules:

- `auth`: registration, login, session context, protected routes.
- `courses`: catalog grid, search/filter state, detail page, enrollment CTA.
- `enrollments`: My Learning list and states.
- `admin`: dashboard shell, CRUD tables/forms, upload handling, confirmation dialogs.

Use React Query or SWR for server state, with cache invalidation after enrollment and admin mutations. Keep the royal-blue luxury design tokens in the frontend only; API responses should remain design-neutral.

## 11. Local development flow

1. Create MySQL database `coursehub` and a least-privileged development user when possible; use `root` only for the initial local setup if required.
2. Copy `.env.example` to local environment files and fill values privately.
3. Install backend dependencies and run Django migrations.
4. Create an admin account through Django management command or `/django-admin/`.
5. Start Django ASGI application for internal services/media/admin.
6. Start FastAPI on a separate local port, for example `8000`.
7. Start React on `5173` with `/api` proxying to FastAPI.

The implementation plan should choose either a single ASGI process mounting FastAPI and Django or two clearly documented processes. For beginner clarity, two processes are preferred initially; a combined deployment can follow after the API contract is stable.

## 12. Testing strategy

- Django model tests for constraints and relationships.
- Service tests for role enforcement, idempotent enrollment, and category/instructor deletion behavior.
- FastAPI endpoint tests for status codes, auth dependencies, validation, and error envelopes.
- React tests for registration, protected routes, search/filter, enrollment state, and admin CRUD feedback.
- One local end-to-end smoke path: register learner → login → browse → enroll → My Learning.

## 13. Architecture risks and mitigations

| Risk | Mitigation |
|---|---|
| Two frameworks drift into duplicate business logic | FastAPI stays thin; Django service layer is canonical. |
| JWT verification differs between services | Share signing configuration and add token contract tests. |
| Root credentials leak into source | Use `.env`, `.env.example` placeholders, and secret scanning. |
| Local media paths break in React | Return absolute API media URLs and add fallback images. |
| Admin role escalation | Ignore role input during registration and create admins separately. |
| Duplicate enrollments under concurrency | Database unique constraint plus atomic service transaction. |

## 14. Decisions requiring approval before implementation

1. Approve Django as the canonical ORM/migration/service owner.
2. Approve FastAPI as the only React-facing API boundary.
3. Approve MySQL environment variables using the provided local credentials without committing secrets.
4. Final decision: run Django and FastAPI as two separate processes during the first implementation.
5. Final decision: use email as the primary login identifier.

## 15. Approval record

Approved by user on 2026-08-20. The approved implementation will use separate Django and FastAPI processes with email-based authentication.

**Status:** Approved

**Next:** Review this architecture, then finalize UX/API details and create implementation epics and stories.
