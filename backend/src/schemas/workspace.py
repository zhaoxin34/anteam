"""Workspace schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WorkspaceCreate(BaseModel):
    """Schema for creating a workspace."""

    name: str
    description: str | None = None


class WorkspaceUpdate(BaseModel):
    """Schema for updating a workspace."""

    name: str | None = None
    description: str | None = None


class WorkspaceResponse(BaseModel):
    """Schema for workspace response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    owner_id: int
    created_at: datetime


class WorkspaceMemberResponse(BaseModel):
    """Schema for workspace member response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    workspace_id: int
    user_id: int
    role: str
    joined_at: datetime


class WorkspaceWithMembers(BaseModel):
    """Schema for workspace with members."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    owner_id: int
    created_at: datetime
    members: list[WorkspaceMemberResponse] = []


class WorkspaceListResponse(BaseModel):
    """Schema for workspace list response."""

    items: list[WorkspaceResponse]
    total: int
