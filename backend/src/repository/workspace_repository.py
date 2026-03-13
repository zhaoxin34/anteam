"""Workspace repository."""

from sqlmodel import Session, delete, select

from ..models.workspace import Workspace, WorkspaceMember
from ..schemas.workspace import WorkspaceCreate, WorkspaceUpdate


class WorkspaceRepository:
    """Workspace repository for data access."""

    def __init__(self, session: Session):
        """Initialize repository with database session."""
        self.session = session

    def get_workspace(self, workspace_id: int) -> Workspace | None:
        """Get workspace by ID."""
        return self.session.get(Workspace, workspace_id)

    def get_user_workspaces(self, user_id: int) -> list[Workspace]:
        """Get all workspaces for a user."""
        # Use a simple subquery approach
        subq = select(WorkspaceMember.workspace_id).where(WorkspaceMember.user_id == user_id)
        statement = select(Workspace).where(Workspace.id.in_(subq))  # type: ignore[union-attr]
        return list(self.session.exec(statement).all())

    def create_workspace(self, workspace_create: WorkspaceCreate, owner_id: int) -> Workspace:
        """Create a new workspace."""
        db_workspace = Workspace(
            name=workspace_create.name,
            description=workspace_create.description,
            owner_id=owner_id,
        )
        self.session.add(db_workspace)
        self.session.flush()  # Get the ID without committing

        # Add owner as member
        member = WorkspaceMember(
            workspace_id=db_workspace.id,
            user_id=owner_id,
            role="owner",
        )
        self.session.add(member)
        self.session.commit()
        self.session.refresh(db_workspace)

        return db_workspace

    def update_workspace(self, workspace_id: int, workspace_update: WorkspaceUpdate) -> Workspace | None:
        """Update a workspace."""
        workspace = self.get_workspace(workspace_id)
        if not workspace:
            return None

        if workspace_update.name is not None:
            workspace.name = workspace_update.name
        if workspace_update.description is not None:
            workspace.description = workspace_update.description

        self.session.add(workspace)
        self.session.commit()
        self.session.refresh(workspace)
        return workspace

    def delete_workspace(self, workspace_id: int) -> bool:
        """Delete a workspace."""
        workspace = self.get_workspace(workspace_id)
        if not workspace:
            return False

        # Delete all members in bulk
        self.session.exec(delete(WorkspaceMember).where(WorkspaceMember.workspace_id == workspace_id))  # type: ignore[arg-type]

        self.session.delete(workspace)
        self.session.commit()
        return True

    def add_member(self, workspace_id: int, user_id: int, role: str = "member") -> WorkspaceMember:
        """Add a member to workspace."""
        # Check if already member
        existing = self.get_member(workspace_id, user_id)
        if existing:
            return existing

        member = WorkspaceMember(
            workspace_id=workspace_id,
            user_id=user_id,
            role=role,
        )
        self.session.add(member)
        self.session.commit()
        self.session.refresh(member)
        return member

    def remove_member(self, workspace_id: int, user_id: int) -> bool:
        """Remove a member from workspace."""
        member = self.get_member(workspace_id, user_id)
        if not member:
            return False

        self.session.delete(member)
        self.session.commit()
        return True

    def get_member(self, workspace_id: int, user_id: int) -> WorkspaceMember | None:
        """Get workspace member."""
        statement = select(WorkspaceMember).where(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == user_id,
        )
        return self.session.exec(statement).first()

    def get_workspace_members(self, workspace_id: int) -> list[WorkspaceMember]:
        """Get all members of a workspace."""
        statement = select(WorkspaceMember).where(WorkspaceMember.workspace_id == workspace_id)
        return list(self.session.exec(statement).all())

    def is_owner(self, workspace_id: int, user_id: int) -> bool:
        """Check if user is workspace owner."""
        workspace = self.get_workspace(workspace_id)
        return workspace is not None and workspace.owner_id == user_id
