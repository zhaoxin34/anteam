"""Channel schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ChannelCreate(BaseModel):
    """Schema for creating a channel."""

    name: str
    description: str | None = None
    workspace_id: int


class ChannelUpdate(BaseModel):
    """Schema for updating a channel."""

    name: str | None = None
    description: str | None = None


class ChannelResponse(BaseModel):
    """Schema for channel response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    workspace_id: int
    owner_id: int
    created_at: datetime


class ChannelMemberResponse(BaseModel):
    """Schema for channel member response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    channel_id: int
    user_id: int
    role: str
    joined_at: datetime


class ChannelWithMembers(BaseModel):
    """Schema for channel with members."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    workspace_id: int
    owner_id: int
    created_at: datetime
    members: list[ChannelMemberResponse] = []


class ChannelListResponse(BaseModel):
    """Schema for channel list response."""

    items: list[ChannelResponse]
    total: int
