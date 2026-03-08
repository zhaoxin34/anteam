"""API dependencies."""

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from ..db.database import get_session
from ..models.user import User
from ..repository.user_repository import UserRepository
from ..service.auth_service import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_db() -> Annotated[Session, Depends]:
    """Get database session."""
    return next(get_session())


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[Session, Depends(get_db)],
) -> User:
    """Get current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_token(token)
    if token_data is None or token_data.username is None:
        raise credentials_exception

    repository = UserRepository(session)
    user = repository.get_user_by_username(token_data.username)
    if user is None:
        raise credentials_exception

    return user
