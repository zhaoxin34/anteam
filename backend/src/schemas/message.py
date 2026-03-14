"""Message schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MessageCreate(BaseModel):
    """Schema for creating a message."""

    content: str
    channel_id: int | None = None
    conversation_id: int | None = None
    parent_id: int | None = None


class MessageUpdate(BaseModel):
    """Schema for updating a message."""

    content: str


class MessageResponse(BaseModel):
    """Schema for message response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    channel_id: int | None
    conversation_id: int | None
    user_id: int
    content: str
    parent_id: int | None
    is_deleted: bool
    created_at: datetime
    updated_at: datetime | None


class MessageListResponse(BaseModel):
    """Schema for message list response."""

    items: list[MessageResponse]
    total: int
