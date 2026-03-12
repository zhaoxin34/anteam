"""Tests for admin API."""

import pytest
from fastapi.testclient import TestClient

# Force import models before app to register tables
from src import models  # noqa: F401
from src.main import app


@pytest.fixture(scope="module")
def _setup_tables():
    """Set up tables once for all tests."""
    from src.db.database import create_db_and_tables

    create_db_and_tables()
    yield


@pytest.fixture
def client(_setup_tables):
    """Create test client."""
    yield TestClient(app)


@pytest.fixture(autouse=True)
def cleanup_db():
    """Clean up database after each test."""
    yield
    # Clean up users table after each test
    from sqlmodel import text

    from src.db.database import engine

    with engine.connect() as conn:
        conn.execute(text("DELETE FROM users"))
        conn.commit()


def get_superuser_token(client: TestClient) -> str:
    """Helper to create and login as superuser."""
    # Register superuser
    client.post(
        "/api/auth/register",
        json={
            "email": "superuser@example.com",
            "username": "superuser",
            "password": "superpass123",
        },
    )
    # Set superuser in DB
    from sqlmodel import text

    from src.db.database import engine

    with engine.connect() as conn:
        conn.execute(text("UPDATE users SET is_superuser = 1 WHERE username = 'superuser'"))
        conn.commit()

    # Login
    response = client.post(
        "/api/auth/login",
        data={"username": "superuser", "password": "superpass123"},
    )
    return response.json()["access_token"]


def get_normal_user_token(client: TestClient) -> str:
    """Helper to create and login as normal user."""
    client.post(
        "/api/auth/register",
        json={
            "email": "normal@example.com",
            "username": "normaluser",
            "password": "normalpass123",
        },
    )
    response = client.post(
        "/api/auth/login",
        data={"username": "normaluser", "password": "normalpass123"},
    )
    return response.json()["access_token"]


class TestAdminAPI:
    """Tests for admin API."""

    def test_get_users_unauthorized(self, client):
        """Test get users without token."""
        response = client.get("/api/admin/users")
        assert response.status_code == 401

    def test_get_users_forbidden_normal_user(self, client):
        """Test get users as normal user."""
        token = get_normal_user_token(client)
        response = client.get(
            "/api/admin/users",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403

    def test_get_users_success(self, client):
        """Test get users as superuser."""
        # Create a test user first
        client.post(
            "/api/auth/register",
            json={
                "email": "testuser@example.com",
                "username": "testuser",
                "password": "testpass123",
            },
        )

        token = get_superuser_token(client)
        response = client.get(
            "/api/admin/users",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert data["total"] >= 2  # superuser + testuser

    def test_create_user_as_superuser(self, client):
        """Test create user as superuser."""
        token = get_superuser_token(client)
        response = client.post(
            "/api/admin/users",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "email": "newuser@example.com",
                "username": "newuser",
                "password": "newpass123",
                "full_name": "New User",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "newuser@example.com"

    def test_update_user_as_superuser(self, client):
        """Test update user as superuser."""
        # Create a user to update
        client.post(
            "/api/auth/register",
            json={
                "email": "toupdate@example.com",
                "username": "toupdate",
                "password": "pass123",
            },
        )

        token = get_superuser_token(client)
        response = client.put(
            "/api/admin/users/2",
            headers={"Authorization": f"Bearer {token}"},
            json={"full_name": "Updated Name", "is_superuser": True},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == "Updated Name"

    def test_delete_user_as_superuser(self, client):
        """Test delete user as superuser."""
        # Create a user to delete
        client.post(
            "/api/auth/register",
            json={
                "email": "todelete@example.com",
                "username": "todelete",
                "password": "pass123",
            },
        )

        token = get_superuser_token(client)
        response = client.delete(
            "/api/admin/users/2",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 204

    def test_get_single_user(self, client):
        """Test get single user."""
        token = get_superuser_token(client)
        response = client.get(
            "/api/admin/users/1",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "username" in data
        assert "email" in data
