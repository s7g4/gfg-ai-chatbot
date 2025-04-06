import pytest
from fastapi.testclient import TestClient
from gfg.backend.test_main import app, test_users

client = TestClient(app)

# Clear test users before each test
@pytest.fixture(autouse=True)
def clear_test_users():
    test_users.clear()

# Test user credentials
TEST_USER = {
    "username": "testuser",
    "password": "testpass123"
}

def register_and_login():
    # Register test user
    response = client.post(
        "/register",
        json={"username": TEST_USER["username"], "password": TEST_USER["password"]},
        headers={"Content-Type": "application/json", "Accept": "application/json"}
    )
    assert response.status_code == 200
    
    # Login to get token
    response = client.post(
        "/login",
        json={"username": TEST_USER["username"], "password": TEST_USER["password"]}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    return response.json()["access_token"]

@pytest.fixture
def auth_token():
    return register_and_login()

def test_emotion_analysis(auth_token):
    response = client.post(
        "/emotion",
        json={"text": "I'm really frustrated with this service!"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "emotion" in data
    assert "confidence" in data
    assert data["emotion"] != ""
    assert data["confidence"] != 0.0

def test_chat(auth_token):
    response = client.post(
        "/chat",
        json={"message": "I want a refund"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert data["response"] != ""

def test_voice_analysis(auth_token):
    mock_audio_data = "UklGRiQAAABXQVZFZm10IBAAAAABAAEAESsAACJWAAACABAAZGF0YQAAAAA="  # Mock base64-encoded audio
    response = client.post(
        "/voice",
        json={"audio": mock_audio_data, "sample_rate": 16000},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "transcript" in data
    assert "sentiment" in data
    assert data["transcript"] != ""
    assert data["sentiment"] != ""
