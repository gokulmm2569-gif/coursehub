"""FastAPI service entrypoint for the CourseHub API boundary."""

import os

import django
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from .admin_routes import router as admin_router
from .auth_routes import router as auth_router
from .catalog_routes import router as catalog_router

app = FastAPI(title="CourseHub API", version="0.1.0", docs_url="/docs")
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:3000').split(','),
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.include_router(auth_router)
app.include_router(catalog_router)
app.include_router(admin_router)


@app.get("/api/v1/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "coursehub-api"}
