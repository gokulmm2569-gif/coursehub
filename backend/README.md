# CourseHub backend foundation

The backend is intentionally split into two local processes:

- Django owns the canonical MySQL models, migrations, authentication, admin, and domain services on port `8000`.
- FastAPI exposes the React-facing versioned API on port `8001`.

## Local setup

1. Create a MySQL database named `coursehub`.
2. Copy `.env.example` to a local `.env` file and set values privately.
3. Create a Python virtual environment and install `backend/requirements.txt`.
4. Run `python backend/manage.py migrate` and create an admin account with `python backend/manage.py createsuperuser`.
5. Optionally seed safe demo catalog data with `python backend/manage.py seed_catalog`.
6. Start Django with `python backend/manage.py runserver 8000`.
7. Start FastAPI with `uvicorn backend.api.main:app --reload --port 8001`.

## Render deployment

The repository includes `render.yaml` for deploying FastAPI with a managed PostgreSQL database. In Render, create a Blueprint from the repository and set `CORS_ALLOWED_ORIGINS` to the deployed Vercel URL, for example `https://coursehub-delta.vercel.app`.

After the first deploy, create an administrator from the Render service shell:

```bash
python manage.py createsuperuser
```

Use the generated Render service URL as Vercel's `COURSEHUB_API_URL` environment variable, then redeploy the frontend.

Epic 2 models: `User`, `Category`, `Instructor`, `Course`, and `Enrollment`. Django is the only owner of schema changes; FastAPI must not introduce a second ORM or migration system.
