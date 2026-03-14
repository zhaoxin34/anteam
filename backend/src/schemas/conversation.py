"""Conversation schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ConversationResponse(BaseModel):
    """Schema for conversation response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user1_id: int
    user2_id: int
    created_at: datetime
    updated_at: datetime


class ConversationListResponse(BaseModel):
    """Schema for conversation list response."""

    items: list[ConversationResponse]
    total: int
