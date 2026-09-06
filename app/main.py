from fastapi import FastAPI

from app.api.routes import posts, comments
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    description="Skeleton API for the Quill blogging platform.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(posts.router, prefix="/api/v1")
app.include_router(comments.router, prefix="/api/v1")
