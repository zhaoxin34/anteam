"""Channel API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from ..api.deps import get_current_user, get_db
from ..models.user import User
from ..repository.channel_repository import ChannelRepository
from ..schemas.channel import (
    ChannelCreate,
    ChannelListResponse,
    ChannelMemberResponse,
    ChannelResponse,
    ChannelUpdate,
)

router = APIRouter(prefix="/api/channels", tags=["channels"])


@router.get("", response_model=ChannelListResponse)
async def list_channels(
    workspace_id: int | None = None,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ChannelListResponse:
    """List all channels for the current user."""
    repository = ChannelRepository(session)
    channels = repository.get_user_channels(current_user.id)  # type: ignore[arg-type]

    if workspace_id:
        channels = [c for c in channels if c.workspace_id == workspace_id]

    return ChannelListResponse(items=channels, total=len(channels))  # type: ignore[arg-type]


@router.post("", response_model=ChannelResponse, status_code=status.HTTP_201_CREATED)
async def create_channel(
    channel_create: ChannelCreate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ChannelResponse:
    """Create a new channel."""
    repository = ChannelRepository(session)
    channel = repository.create_channel(channel_create, current_user.id)  # type: ignore[arg-type]
    return channel  # type: ignore[return-value]


@router.get("/{channel_id}", response_model=ChannelResponse)
async def get_channel(
    channel_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ChannelResponse:
    """Get a channel by ID."""
    repository = ChannelRepository(session)

    # Check if user is member
    if not repository.is_member(channel_id, current_user.id):  # type: ignore[arg-type]
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found",
        )

    channel = repository.get_channel(channel_id)
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found",
        )
    return channel  # type: ignore[return-value]


@router.put("/{channel_id}", response_model=ChannelResponse)
async def update_channel(
    channel_id: int,
    channel_update: ChannelUpdate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ChannelResponse:
    """Update a channel."""
    repository = ChannelRepository(session)

    # Check ownership
    if not repository.is_owner(channel_id, current_user.id):  # type: ignore[arg-type]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    channel = repository.update_channel(channel_id, channel_update)
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found",
        )
    return channel  # type: ignore[return-value]


@router.delete("/{channel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_channel(
    channel_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete a channel."""
    repository = ChannelRepository(session)

    # Check ownership
    if not repository.is_owner(channel_id, current_user.id):  # type: ignore[arg-type]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    success = repository.delete_channel(channel_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found",
        )


@router.post("/{channel_id}/join", response_model=ChannelResponse)
async def join_channel(
    channel_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ChannelResponse:
    """Join a channel."""
    repository = ChannelRepository(session)

    # Check if channel exists
    channel = repository.get_channel(channel_id)
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found",
        )

    # Add member
    repository.add_member(channel_id, current_user.id)  # type: ignore[arg-type]

    return channel  # type: ignore[return-value]


@router.post("/{channel_id}/leave", status_code=status.HTTP_204_NO_CONTENT)
async def leave_channel(
    channel_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Leave a channel."""
    repository = ChannelRepository(session)

    # Check if user is member
    if not repository.is_member(channel_id, current_user.id):  # type: ignore[arg-type]
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not a member of this channel",
        )

    # Check if user is owner
    if repository.is_owner(channel_id, current_user.id):  # type: ignore[arg-type]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Owner cannot leave channel. Transfer ownership first.",
        )

    success = repository.remove_member(channel_id, current_user.id)  # type: ignore[arg-type]
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found",
        )


@router.get("/{channel_id}/members", response_model=list[ChannelMemberResponse])
async def list_channel_members(
    channel_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ChannelMemberResponse]:
    """List all members of a channel."""
    repository = ChannelRepository(session)

    # Check if user is member
    if not repository.is_member(channel_id, current_user.id):  # type: ignore[arg-type]
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Channel not found",
        )

    members = repository.get_channel_members(channel_id)
    return members  # type: ignore[return-value]


@router.delete("/{channel_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(
    channel_id: int,
    user_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Remove a member from channel."""
    repository = ChannelRepository(session)

    # Check ownership
    if not repository.is_owner(channel_id, current_user.id):  # type: ignore[arg-type]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    success = repository.remove_member(channel_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found",
        )
