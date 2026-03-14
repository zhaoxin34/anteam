"""Message API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from ..api.deps import get_current_user, get_db
from ..models.user import User
from ..repository.channel_repository import ChannelRepository
from ..repository.message_repository import MessageRepository
from ..schemas.message import (
    MessageCreate,
    MessageListResponse,
    MessageResponse,
    MessageUpdate,
)

router = APIRouter(prefix="/api", tags=["messages"])


@router.get("/channels/{channel_id}/messages", response_model=MessageListResponse)
async def get_channel_messages(
    channel_id: int,
    limit: int = 50,
    offset: int = 0,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> MessageListResponse:
    """Get messages for a channel."""
    # Check if user is channel member
    channel_repo = ChannelRepository(session)
    if not channel_repo.is_member(channel_id, current_user.id):  # type: ignore[arg-type]
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found",
        )

    message_repo = MessageRepository(session)
    messages = message_repo.get_channel_messages(channel_id, limit, offset)
    total = message_repo.get_channel_messages_count(channel_id)

    return MessageListResponse(items=messages, total=total)  # type: ignore[arg-type]


@router.post("/channels/{channel_id}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(
    channel_id: int,
    message_create: MessageCreate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> MessageResponse:
    """Create a new message in a channel."""
    # Check if user is channel member
    channel_repo = ChannelRepository(session)
    if not channel_repo.is_member(channel_id, current_user.id):  # type: ignore[arg-type]
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found",
        )

    # Set channel_id from path
    message_create.channel_id = channel_id

    message_repo = MessageRepository(session)
    message = message_repo.create_message(message_create, current_user.id)  # type: ignore[arg-type]
    return message  # type: ignore[return-value]


@router.put("/messages/{message_id}", response_model=MessageResponse)
async def update_message(
    message_id: int,
    message_update: MessageUpdate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> MessageResponse:
    """Update a message."""
    message_repo = MessageRepository(session)
    message = message_repo.get_message(message_id)

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )

    # Check ownership
    if message.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    updated = message_repo.update_message(message_id, message_update)
    return updated  # type: ignore[return-value]


@router.delete("/messages/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(
    message_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete a message."""
    message_repo = MessageRepository(session)
    message = message_repo.get_message(message_id)

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )

    # Check ownership
    if message.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    message_repo.delete_message(message_id)


@router.get("/messages/{message_id}/replies", response_model=MessageListResponse)
async def get_message_replies(
    message_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> MessageListResponse:
    """Get replies to a message (thread)."""
    message_repo = MessageRepository(session)
    message = message_repo.get_message(message_id)

    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Message not found",
        )

    # Check if user is channel member
    if message.channel_id:
        channel_repo = ChannelRepository(session)
        if not channel_repo.is_member(message.channel_id, current_user.id):  # type: ignore[arg-type]
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Channel not found",
            )

    replies = message_repo.get_thread_replies(message_id)
    return MessageListResponse(items=replies, total=len(replies))  # type: ignore[arg-type]
