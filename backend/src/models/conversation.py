"""Conversation data models."""

from datetime import datetime

from sqlmodel import Field, SQLModel


class Conversation(SQLModel, table=True):
    """Conversation model for DM."""

    __tablename__ = "conversations"

    id: int | None = Field(default=None, primary_key=True)
    user1_id: int = Field(foreign_key="users.id")
    user2_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
