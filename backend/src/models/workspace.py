"""Workspace data models."""

from datetime import datetime

from sqlmodel import Field, SQLModel


class Workspace(SQLModel, table=True):
    """Workspace model."""

    __tablename__ = "workspaces"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str | None = None
    owner_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class WorkspaceMember(SQLModel, table=True):
    """Workspace member model."""

    __tablename__ = "workspace_members"

    id: int | None = Field(default=None, primary_key=True)
    workspace_id: int = Field(foreign_key="workspaces.id")
    user_id: int = Field(foreign_key="users.id")
    role: str = Field(default="member")  # owner, admin, member
    joined_at: datetime = Field(default_factory=datetime.utcnow)
