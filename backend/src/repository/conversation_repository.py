"""Conversation repository."""

from datetime import datetime

from sqlmodel import select

from ..models.conversation import Conversation


class ConversationRepository:
    """Conversation repository for data access."""

    def __init__(self, session):
        """Initialize repository with database session."""
        self.session = session

    def get_or_create_conversation(self, user1_id: int, user2_id: int) -> Conversation:
        """Get or create a conversation between two users."""
        # Ensure user1_id < user2_id for consistency
        if user1_id > user2_id:
            user1_id, user2_id = user2_id, user1_id

        # Check if conversation exists
        statement = select(Conversation).where(
            Conversation.user1_id == user1_id,
            Conversation.user2_id == user2_id,
        )
        existing = self.session.exec(statement).first()

        if existing:
            return existing

        # Create new conversation
        conversation = Conversation(
            user1_id=user1_id,
            user2_id=user2_id,
        )
        self.session.add(conversation)
        self.session.commit()
        self.session.refresh(conversation)
        return conversation

    def get_user_conversations(self, user_id: int) -> list[Conversation]:
        """Get all conversations for a user."""
        statement = select(Conversation).where((Conversation.user1_id == user_id) | (Conversation.user2_id == user_id)).order_by(Conversation.updated_at.desc())
        return list(self.session.exec(statement).all())  # type: ignore[no-any-return]

    def get_conversation(self, conversation_id: int) -> Conversation | None:
        """Get conversation by ID."""
        return self.session.get(Conversation, conversation_id)

    def get_conversation_by_users(self, user1_id: int, user2_id: int) -> Conversation | None:
        """Get conversation by user IDs."""
        # Ensure user1_id < user2_id
        if user1_id > user2_id:
            user1_id, user2_id = user2_id, user1_id

        statement = select(Conversation).where(
            Conversation.user1_id == user1_id,
            Conversation.user2_id == user2_id,
        )
        return self.session.exec(statement).first()

    def update_conversation_timestamp(self, conversation_id: int):
        """Update conversation's updated_at timestamp."""
        conversation = self.get_conversation(conversation_id)
        if conversation:
            conversation.updated_at = datetime.utcnow()
            self.session.add(conversation)
            self.session.commit()

    def is_participant(self, conversation_id: int, user_id: int) -> bool:
        """Check if user is a participant in the conversation."""
        conversation = self.get_conversation(conversation_id)
        if not conversation:
            return False
        return conversation.user1_id == user_id or conversation.user2_id == user_id
