"""Workspace API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from ..api.deps import get_current_user, get_db
from ..models.user import User
from ..repository.workspace_repository import WorkspaceRepository
from ..schemas.workspace import (
    WorkspaceCreate,
    WorkspaceListResponse,
    WorkspaceMemberResponse,
    WorkspaceResponse,
    WorkspaceUpdate,
)

router = APIRouter(prefix="/api/workspaces", tags=["workspaces"])


@router.get("", response_model=WorkspaceListResponse)
async def list_workspaces(
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> WorkspaceListResponse:
    """List all workspaces for the current user."""
    repository = WorkspaceRepository(session)
    workspaces = repository.get_user_workspaces(current_user.id)  # type: ignore[arg-type]
    return WorkspaceListResponse(items=workspaces, total=len(workspaces))  # type: ignore[arg-type]


@router.post("", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
async def create_workspace(
    workspace_create: WorkspaceCreate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> WorkspaceResponse:
    """Create a new workspace."""
    repository = WorkspaceRepository(session)
    workspace = repository.create_workspace(workspace_create, current_user.id)  # type: ignore[arg-type]
    return workspace  # type: ignore[return-value]


@router.get("/{workspace_id}", response_model=WorkspaceResponse)
async def get_workspace(
    workspace_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> WorkspaceResponse:
    """Get a workspace by ID."""
    repository = WorkspaceRepository(session)

    # Check if user is member
    member = repository.get_member(workspace_id, current_user.id)  # type: ignore[arg-type]
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found",
        )

    workspace = repository.get_workspace(workspace_id)
    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found",
        )
    return workspace  # type: ignore[return-value]


@router.put("/{workspace_id}", response_model=WorkspaceResponse)
async def update_workspace(
    workspace_id: int,
    workspace_update: WorkspaceUpdate,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> WorkspaceResponse:
    """Update a workspace."""
    repository = WorkspaceRepository(session)

    # Check ownership
    if not repository.is_owner(workspace_id, current_user.id):  # type: ignore[arg-type]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    workspace = repository.update_workspace(workspace_id, workspace_update)
    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found",
        )
    return workspace  # type: ignore[return-value]


@router.delete("/{workspace_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workspace(
    workspace_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete a workspace."""
    repository = WorkspaceRepository(session)

    # Check ownership
    if not repository.is_owner(workspace_id, current_user.id):  # type: ignore[arg-type]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    success = repository.delete_workspace(workspace_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found",
        )


@router.post("/{workspace_id}/join", response_model=WorkspaceResponse)
async def join_workspace(
    workspace_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> WorkspaceResponse:
    """Join a workspace."""
    repository = WorkspaceRepository(session)

    # Check if workspace exists
    workspace = repository.get_workspace(workspace_id)
    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found",
        )

    # Add member
    repository.add_member(workspace_id, current_user.id)  # type: ignore[arg-type]

    return workspace  # type: ignore[return-value]


@router.delete("/{workspace_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(
    workspace_id: int,
    user_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Remove a member from workspace."""
    repository = WorkspaceRepository(session)

    # Check ownership
    if not repository.is_owner(workspace_id, current_user.id):  # type: ignore[arg-type]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    success = repository.remove_member(workspace_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found",
        )


@router.post("/{workspace_id}/leave", status_code=status.HTTP_204_NO_CONTENT)
async def leave_workspace(
    workspace_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Leave a workspace."""
    repository = WorkspaceRepository(session)

    # Check if user is member
    member = repository.get_member(workspace_id, current_user.id)  # type: ignore[arg-type]
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not a member of this workspace",
        )

    # Check if user is owner
    if repository.is_owner(workspace_id, current_user.id):  # type: ignore[arg-type]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Owner cannot leave workspace. Transfer ownership first.",
        )

    success = repository.remove_member(workspace_id, current_user.id)  # type: ignore[arg-type]
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found",
        )


@router.get("/{workspace_id}/members", response_model=list[WorkspaceMemberResponse])
async def list_workspace_members(
    workspace_id: int,
    session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[WorkspaceMemberResponse]:
    """List all members of a workspace."""
    repository = WorkspaceRepository(session)

    # Check if user is member
    member = repository.get_member(workspace_id, current_user.id)  # type: ignore[arg-type]
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found",
        )

    members = repository.get_workspace_members(workspace_id)
    return members  # type: ignore[return-value]
