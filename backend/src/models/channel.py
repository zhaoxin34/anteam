"""Channel data models."""

from datetime import datetime

from sqlmodel import Field, SQLModel


class Channel(SQLModel, table=True):
    """Channel model."""

    __tablename__ = "channels"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str | None = None
    workspace_id: int = Field(foreign_key="workspaces.id")
    owner_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ChannelMember(SQLModel, table=True):
    """Channel member model."""

    __tablename__ = "channel_members"

    id: int | None = Field(default=None, primary_key=True)
    channel_id: int = Field(foreign_key="channels.id")
    user_id: int = Field(foreign_key="users.id")
    role: str = Field(default="member")  # owner, admin, member
    joined_at: datetime = Field(default_factory=datetime.utcnow)
