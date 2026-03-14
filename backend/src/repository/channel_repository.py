"""Channel repository."""

from sqlmodel import Session, delete, select

from ..models.channel import Channel, ChannelMember
from ..models.workspace import WorkspaceMember
from ..schemas.channel import ChannelCreate, ChannelUpdate


class ChannelRepository:
    """Channel repository for data access."""

    def __init__(self, session: Session):
        """Initialize repository with database session."""
        self.session = session

    def get_channel(self, channel_id: int) -> Channel | None:
        """Get channel by ID."""
        return self.session.get(Channel, channel_id)

    def get_user_channels(self, user_id: int) -> list[Channel]:
        """Get all channels for a user."""
        # Get workspace IDs user is member of
        workspace_subq = select(WorkspaceMember.workspace_id).where(WorkspaceMember.user_id == user_id)
        # Get channels in those workspaces
        statement = select(Channel).where(Channel.workspace_id.in_(workspace_subq))
        # type: ignore[no-any-return]
        return list(self.session.exec(statement).all())

    def create_channel(self, channel_create: ChannelCreate, owner_id: int) -> Channel:
        """Create a new channel."""
        db_channel = Channel(
            name=channel_create.name,
            description=channel_create.description,
            workspace_id=channel_create.workspace_id,
            owner_id=owner_id,
        )
        self.session.add(db_channel)
        self.session.flush()

        # Add owner as member
        member = ChannelMember(
            channel_id=db_channel.id,
            user_id=owner_id,
            role="owner",
        )
        self.session.add(member)
        self.session.commit()
        self.session.refresh(db_channel)

        return db_channel

    def update_channel(self, channel_id: int, channel_update: ChannelUpdate) -> Channel | None:
        """Update a channel."""
        channel = self.get_channel(channel_id)
        if not channel:
            return None

        if channel_update.name is not None:
            channel.name = channel_update.name
        if channel_update.description is not None:
            channel.description = channel_update.description

        self.session.add(channel)
        self.session.commit()
        self.session.refresh(channel)
        return channel

    def delete_channel(self, channel_id: int) -> bool:
        """Delete a channel."""
        channel = self.get_channel(channel_id)
        if not channel:
            return False

        # Delete all members in bulk
        self.session.exec(delete(ChannelMember).where(ChannelMember.channel_id == channel_id))  # type: ignore[arg-type]

        self.session.delete(channel)
        self.session.commit()
        return True

    def add_member(self, channel_id: int, user_id: int, role: str = "member") -> ChannelMember:
        """Add a member to channel."""
        # Check if already member
        existing = self.get_member(channel_id, user_id)
        if existing:
            return existing

        member = ChannelMember(
            channel_id=channel_id,
            user_id=user_id,
            role=role,
        )
        self.session.add(member)
        self.session.commit()
        self.session.refresh(member)
        return member

    def remove_member(self, channel_id: int, user_id: int) -> bool:
        """Remove a member from channel."""
        member = self.get_member(channel_id, user_id)
        if not member:
            return False

        self.session.delete(member)
        self.session.commit()
        return True

    def get_member(self, channel_id: int, user_id: int) -> ChannelMember | None:
        """Get channel member."""
        statement = select(ChannelMember).where(
            ChannelMember.channel_id == channel_id,
            ChannelMember.user_id == user_id,
        )
        return self.session.exec(statement).first()

    def get_channel_members(self, channel_id: int) -> list[ChannelMember]:
        """Get all members of a channel."""
        statement = select(ChannelMember).where(ChannelMember.channel_id == channel_id)
        return list(self.session.exec(statement).all())  # type: ignore[no-any-return]

    def is_member(self, channel_id: int, user_id: int) -> bool:
        """Check if user is channel member."""
        return self.get_member(channel_id, user_id) is not None

    def is_owner(self, channel_id: int, user_id: int) -> bool:
        """Check if user is channel owner."""
        channel = self.get_channel(channel_id)
        return channel is not None and channel.owner_id == user_id
