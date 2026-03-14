"""Main application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.admin import router as admin_router
from .api.auth import router as auth_router
from .api.channel import router as channel_router
from .api.dm import router as dm_router
from .api.message import router as message_router
from .api.websocket import router as websocket_router
from .api.workspace import router as workspace_router
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

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(workspace_router)
app.include_router(channel_router)
app.include_router(message_router)
app.include_router(dm_router)
app.include_router(websocket_router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}
