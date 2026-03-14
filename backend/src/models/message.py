"""Message data models."""

from datetime import datetime

from sqlmodel import Field, SQLModel


class Message(SQLModel, table=True):
    """Message model."""

    __tablename__ = "messages"

    id: int | None = Field(default=None, primary_key=True)
    channel_id: int | None = Field(default=None, foreign_key="channels.id")
    conversation_id: int | None = Field(default=None, foreign_key="conversations.id")
    user_id: int = Field(foreign_key="users.id")
    content: str
    parent_id: int | None = Field(default=None, foreign_key="messages.id")
    is_deleted: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(default=None)
