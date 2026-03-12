"""Admin API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, func, select

from ..api.deps import get_current_superuser, get_db
from ..models.user import User
from ..repository.user_repository import UserRepository
from ..schemas.user_admin import (
    UserAdminCreate,
    UserAdminResponse,
    UserAdminUpdate,
    UserListResponse,
)

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/users", response_model=UserListResponse)
async def get_users(
    page: int = 1,
    page_size: int = 20,
    session: Session = Depends(get_db),
    _: User = Depends(get_current_superuser),
) -> UserListResponse:
    """Get paginated list of users."""
    offset = (page - 1) * page_size

    # Get total count
    count_statement = select(func.count()).select_from(User)
    total = session.exec(count_statement).one()

    # Get users
    statement = select(User).offset(offset).limit(page_size)
    users = session.exec(statement).all()

    return UserListResponse(
        items=[UserAdminResponse.model_validate(u) for u in users],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/users/{user_id}", response_model=UserAdminResponse)
async def get_user(
    user_id: int,
    session: Session = Depends(get_db),
    _: User = Depends(get_current_superuser),
) -> UserAdminResponse:
    """Get a single user by ID."""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user  # type: ignore[return-value]


@router.post("/users", response_model=UserAdminResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_create: UserAdminCreate,
    session: Session = Depends(get_db),
    _: User = Depends(get_current_superuser),
) -> UserAdminResponse:
    """Create a new user."""
    repository = UserRepository(session)

    # Check if email already exists
    if repository.get_user_by_email(user_create.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Check if username already exists
    if repository.get_user_by_username(user_create.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )

    # Create user
    from ..service.auth_service import get_password_hash

    hashed_password = get_password_hash(user_create.password)
    db_user = User(
        email=user_create.email,
        username=user_create.username,
        hashed_password=hashed_password,
        full_name=user_create.full_name,
        is_active=user_create.is_active,
        is_superuser=user_create.is_superuser,
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user  # type: ignore[return-value]


@router.put("/users/{user_id}", response_model=UserAdminResponse)
async def update_user(
    user_id: int,
    user_update: UserAdminUpdate,
    session: Session = Depends(get_db),
    _: User = Depends(get_current_superuser),
) -> UserAdminResponse:
    """Update a user."""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    repository = UserRepository(session)

    # Check email uniqueness if changing
    if user_update.email and user_update.email != user.email:
        if repository.get_user_by_email(user_update.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        user.email = user_update.email

    # Check username uniqueness if changing
    if user_update.username and user_update.username != user.username:
        if repository.get_user_by_username(user_update.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )
        user.username = user_update.username

    # Update other fields
    if user_update.full_name is not None:
        user.full_name = user_update.full_name
    if user_update.is_active is not None:
        user.is_active = user_update.is_active
    if user_update.is_superuser is not None:
        user.is_superuser = user_update.is_superuser

    session.add(user)
    session.commit()
    session.refresh(user)

    return user  # type: ignore[return-value]


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    session: Session = Depends(get_db),
    _: User = Depends(get_current_superuser),
) -> None:
    """Delete a user."""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    session.delete(user)
    session.commit()
