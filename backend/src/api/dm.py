"""DM API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from ..api.deps import get_current_user, get_db
from ..models.user import User
from ..repository.conversation_repository import ConversationRepository
from ..repository.message_repository import MessageRepository
from ..schemas.conversation import ConversationListResponse, ConversationResponse
from ..schemas.message import MessageCreate, MessageListResponse, MessageResponse

router = APIRouter(prefix="/api", tags=["dm"])


@router.get("/conversations", response_model=ConversationListResponse)
async def list_conversations(
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ConversationListResponse:
    """List all conversations for the current user."""
    repository = ConversationRepository(session)
    conversations = repository.get_user_conversations(current_user.id)  # type: ignore[arg-type]
    return ConversationListResponse(items=conversations, total=len(conversations))  # type: ignore[arg-type]


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ConversationResponse:
    """Get a conversation by ID."""
    repository = ConversationRepository(session)
    conversation = repository.get_conversation(conversation_id)

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    # Check if user is participant
    if not repository.is_participant(conversation_id, current_user.id):  # type: ignore[arg-type]
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    return conversation  # type: ignore[return-value]


@router.get("/conversations/{conversation_id}/messages", response_model=MessageListResponse)
async def get_conversation_messages(
    conversation_id: int,
    limit: int = 50,
    offset: int = 0,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> MessageListResponse:
    """Get messages for a conversation."""
    conv_repo = ConversationRepository(session)

    # Check if user is participant
    if not conv_repo.is_participant(conversation_id, current_user.id):  # type: ignore[arg-type]
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    message_repo = MessageRepository(session)
    messages = message_repo.get_conversation_messages(conversation_id, limit, offset)
    total = message_repo.get_conversation_messages_count(conversation_id)

    return MessageListResponse(items=messages, total=total)  # type: ignore[arg-type]


@router.post("/conversations/{conversation_id}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation_message(
    conversation_id: int,
    message_create: MessageCreate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> MessageResponse:
    """Create a new message in a conversation."""
    conv_repo = ConversationRepository(session)

    # Check if user is participant
    if not conv_repo.is_participant(conversation_id, current_user.id):  # type: ignore[arg-type]
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    # Set conversation_id and clear channel_id
    message_create.conversation_id = conversation_id
    message_create.channel_id = None

    message_repo = MessageRepository(session)
    message = message_repo.create_message(message_create, current_user.id)  # type: ignore[arg-type]

    # Update conversation timestamp
    conv_repo.update_conversation_timestamp(conversation_id)

    return message  # type: ignore[return-value]


@router.post("/users/{user_id}/message", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def start_or_get_dm(
    user_id: int,
    message_create: MessageCreate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> MessageResponse:
    """Start a new DM or send message to a user."""
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot send message to yourself",
        )

    # Get or create conversation
    conv_repo = ConversationRepository(session)
    conversation = conv_repo.get_or_create_conversation(current_user.id, user_id)

    # Create message
    message_create.conversation_id = conversation.id
    message_create.channel_id = None

    message_repo = MessageRepository(session)
    message = message_repo.create_message(message_create, current_user.id)  # type: ignore[arg-type]

    # Update conversation timestamp
    conv_repo.update_conversation_timestamp(conversation.id)

    return message  # type: ignore[return-value]
