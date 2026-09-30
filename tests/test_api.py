import pytest
import requests
import time


# Base URL for API tests
BASE_URL = "http://localhost:5000/api"


@pytest.fixture
def base_url():
    """Fixture providing the base URL for API tests"""
    return BASE_URL


@pytest.fixture
def auth_token():
    """Fixture that registers a user and returns auth token"""

    # Create unique username using timestamp
    timestamp = int(time.time() * 1000)
    username = f"testuser_{timestamp}"

    # Register user
    user_data = {
        "username": username,
        "password": "testpass123"
    }

    requests.post(f"{BASE_URL}/auth/register", json=user_data)

    # Login and get token
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json=user_data
    )

    token = response.json()["access_token"]

    return token

def test_health_check():
    """Test that the health endpoint returns healthy status"""

    # Act: Make request to health endpoint
    response = requests.get(f"{BASE_URL}/health")

    # Assert: Check status code
    assert response.status_code == 200

    # Assert: Check response body
    data = response.json()
    assert data["status"] == "healthy"


def test_create_event(auth_token):
    """Test creating a public event"""

    # Arrange: Event data
    event_data = {
        "title": "Python Meetup",
        "description": "A meetup for Python developers",
        "date": "2026-10-15T18:00:00",
        "location": "Stuttgart",
        "capacity": 50,
        "is_public": True,
        "requires_admin": False
    }

    # Act: Create event
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }

    response = requests.post(
        f"{BASE_URL}/events",
        json=event_data,
        headers=headers
    )

    # Assert: Check response status
    assert response.status_code == 201

    # Assert: Check response body
    data = response.json()

    assert data["title"] == event_data["title"]
    assert data["description"] == event_data["description"]
    assert data["location"] == event_data["location"]
    assert data["capacity"] == event_data["capacity"]
    assert data["is_public"] == event_data["is_public"]
    assert data["requires_admin"] == event_data["requires_admin"]
    assert "id" in data