"""Message repository."""

from datetime import datetime

from sqlmodel import func, select

from ..models.message import Message
from ..schemas.message import MessageCreate, MessageUpdate


class MessageRepository:
    """Message repository for data access."""

    def __init__(self, session):
        """Initialize repository with database session."""
        self.session = session

    def create_message(self, message_create: MessageCreate, user_id: int) -> Message:
        """Create a new message."""
        db_message = Message(
            channel_id=message_create.channel_id,
            conversation_id=getattr(message_create, "conversation_id", None),
            user_id=user_id,
            content=message_create.content,
            parent_id=message_create.parent_id,
        )
        self.session.add(db_message)
        self.session.commit()
        self.session.refresh(db_message)
        return db_message

    def get_message(self, message_id: int) -> Message | None:
        """Get message by ID."""
        return self.session.get(Message, message_id)

    def get_channel_messages(self, channel_id: int, limit: int = 50, offset: int = 0) -> list[Message]:
        """Get messages for a channel."""
        statement = (
            select(Message)
            .where(Message.channel_id == channel_id)
            .where(not Message.is_deleted)
            .where(Message.parent_id is None)  # Only top-level messages
            .order_by(Message.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        # type: ignore[no-any-return]
        return list(self.session.exec(statement).all())

    def get_channel_messages_count(self, channel_id: int) -> int:
        """Get total count of channel messages."""
        statement = select(func.count(Message.id)).where(Message.channel_id == channel_id).where(not Message.is_deleted).where(Message.parent_id is None)
        # type: ignore[no-any-return]
        return self.session.exec(statement).one()

    def update_message(self, message_id: int, message_update: MessageUpdate) -> Message | None:
        """Update a message."""
        message = self.get_message(message_id)
        if not message:
            return None

        message.content = message_update.content
        message.updated_at = datetime.utcnow()

        self.session.add(message)
        self.session.commit()
        self.session.refresh(message)
        return message

    def delete_message(self, message_id: int) -> bool:
        """Delete a message (soft delete)."""
        message = self.get_message(message_id)
        if not message:
            return False

        message.is_deleted = True
        self.session.add(message)
        self.session.commit()
        return True

    def get_thread_replies(self, message_id: int) -> list[Message]:
        """Get replies to a message (thread)."""
        statement = select(Message).where(Message.parent_id == message_id).where(not Message.is_deleted).order_by(Message.created_at.asc())
        # type: ignore[no-any-return]
        return list(self.session.exec(statement).all())

    def get_reply_count(self, message_id: int) -> int:
        """Get count of replies to a message."""
        statement = select(func.count(Message.id)).where(Message.parent_id == message_id).where(not Message.is_deleted)
        # type: ignore[no-any-return]
        return self.session.exec(statement).one()

    def get_conversation_messages(self, conversation_id: int, limit: int = 50, offset: int = 0) -> list[Message]:
        """Get messages for a conversation."""
        statement = select(Message).where(Message.conversation_id == conversation_id).where(not Message.is_deleted).order_by(Message.created_at.desc()).limit(limit).offset(offset)
        # type: ignore[no-any-return]
        return list(self.session.exec(statement).all())

    def get_conversation_messages_count(self, conversation_id: int) -> int:
        """Get total count of conversation messages."""
        statement = select(func.count(Message.id)).where(Message.conversation_id == conversation_id).where(not Message.is_deleted)
        # type: ignore[no-any-return]
        return self.session.exec(statement).one()
