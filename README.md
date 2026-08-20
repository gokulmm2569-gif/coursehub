# CourseHub

CourseHub is a premium learning platform built with a React frontend, Django core service, FastAPI API service, and MySQL.

## Foundation status

Epic 1 establishes the repository boundaries and local configuration contract. The current visual React experience runs from the root Next.js app while `frontend/` reserves the standalone client boundary for the API integration slice.

## Services

| Service | Responsibility | Port |
| --- | --- | --- |
| React/Next.js | Premium royal-blue learner interface | 3000 |
| Django | ORM, migrations, auth, admin, domain services | 8000 |
| FastAPI | Versioned frontend API and health checks | 8001 |
| MySQL | Persistent application data | 3306 |

## Local configuration

Copy `.env.example` to `.env` and fill in private local values. Never commit passwords, JWT secrets, or `.env` files. The supplied MySQL credentials are local-only configuration and are not included in this repository.

## Start order

1. Start MySQL and create the `coursehub` database.
2. Start Django after its project scaffold and migrations are available.
3. Start FastAPI: `uvicorn backend.api.main:app --reload --port 8001`.
4. Start the React experience with `pnpm dev`.

See `backend/README.md` for backend-specific setup. The next epics add Django models, migrations, authentication, and API contracts.
