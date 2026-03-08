"""User repository."""

from sqlmodel import Session, select

from ..models.user import User
from ..schemas.user import UserCreate
from ..service.auth_service import get_password_hash


class UserRepository:
    """User repository for data access."""

    def __init__(self, session: Session):
        """Initialize repository with database session."""
        self.session = session

    def get_user_by_email(self, email: str) -> User | None:
        """Get user by email."""
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()

    def get_user_by_username(self, username: str) -> User | None:
        """Get user by username."""
        statement = select(User).where(User.username == username)
        return self.session.exec(statement).first()

    def get_user(self, user_id: int) -> User | None:
        """Get user by ID."""
        return self.session.get(User, user_id)

    def create_user(self, user_create: UserCreate) -> User:
        """Create a new user."""
        hashed_password = get_password_hash(user_create.password)
        db_user = User(
            email=user_create.email,
            username=user_create.username,
            hashed_password=hashed_password,
            full_name=user_create.full_name,
        )
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user
