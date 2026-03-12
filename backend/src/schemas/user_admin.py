"""Admin schemas for user management."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserAdminCreate(BaseModel):
    """Schema for admin to create user."""

    email: EmailStr
    username: str
    password: str
    full_name: str | None = None
    is_active: bool = True
    is_superuser: bool = False


class UserAdminUpdate(BaseModel):
    """Schema for admin to update user."""

    email: EmailStr | None = None
    username: str | None = None
    full_name: str | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None


class UserAdminResponse(BaseModel):
    """Schema for admin user response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    username: str
    full_name: str | None
    is_active: bool
    is_superuser: bool
    created_at: datetime


class UserListResponse(BaseModel):
    """Schema for paginated user list."""

    items: list[UserAdminResponse]
    total: int
    page: int
    page_size: int
