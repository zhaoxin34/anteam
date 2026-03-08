"""Tests for authentication."""

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


class TestAuthAPI:
    """Tests for auth API."""

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_register_user(self, client):
        """Test user registration."""
        response = client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "testpass123",
                "full_name": "Test User",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["username"] == "testuser"
        assert data["full_name"] == "Test User"
        assert "id" in data

    def test_register_duplicate_email(self, client):
        """Test registration with duplicate email."""
        # Register first user
        client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser1",
                "password": "testpass123",
            },
        )

        # Try to register with same email
        response = client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser2",
                "password": "testpass123",
            },
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "Email already registered"

    def test_register_duplicate_username(self, client):
        """Test registration with duplicate username."""
        # Register first user
        client.post(
            "/api/auth/register",
            json={
                "email": "test1@example.com",
                "username": "testuser",
                "password": "testpass123",
            },
        )

        # Try to register with same username
        response = client.post(
            "/api/auth/register",
            json={
                "email": "test2@example.com",
                "username": "testuser",
                "password": "testpass123",
            },
        )
        assert response.status_code == 400
        assert response.json()["detail"] == "Username already taken"

    def test_login_success(self, client):
        """Test successful login."""
        # Register user first
        client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "testpass123",
            },
        )

        # Login
        response = client.post(
            "/api/auth/login",
            data={"username": "testuser", "password": "testpass123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client):
        """Test login with wrong password."""
        # Register user first
        client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "testpass123",
            },
        )

        # Login with wrong password
        response = client.post(
            "/api/auth/login",
            data={"username": "testuser", "password": "wrongpassword"},
        )
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client):
        """Test login with nonexistent user."""
        response = client.post(
            "/api/auth/login",
            data={"username": "nonexistent", "password": "testpass123"},
        )
        assert response.status_code == 401

    def test_get_current_user(self, client):
        """Test get current user endpoint."""
        # Register user first
        client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "testpass123",
            },
        )

        # Login to get token
        login_response = client.post(
            "/api/auth/login",
            data={"username": "testuser", "password": "testpass123"},
        )
        token = login_response.json()["access_token"]

        # Get current user
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"

    def test_get_current_user_unauthorized(self, client):
        """Test get current user without token."""
        response = client.get("/api/auth/me")
        assert response.status_code == 401
