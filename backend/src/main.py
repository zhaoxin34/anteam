"""Main application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api.auth import router as auth_router
from .core.config import settings
from .db.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    create_db_and_tables()
    yield
    # Shutdown


app = FastAPI(
    title=settings.app_name,
    description="Slack-style chat system",
    version="0.1.0",
    lifespan=lifespan,
)

# Include routers
app.include_router(auth_router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}
