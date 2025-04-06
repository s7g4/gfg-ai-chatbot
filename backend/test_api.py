import pytest
from fastapi.testclient import TestClient
from main import app
import os
from dotenv import load_dotenv

load_dotenv()

client = TestClient(app)

# Test data
TEST_USER = {
    "username": "testuser",
    "password": "testpassword123"
}

def test_register_user():
    # Clean up test user if exists
    from pymongo import MongoClient
    mongo_client = MongoClient(os.getenv("MONGO_URI"))
    db = mongo_client[os.getenv("DATABASE_NAME")]
    db.users.delete_one({"username": TEST_USER["username"]})
    
    # Register new user
    response = client.post("/register", json=TEST_USER)
    assert response.status_code == 200
    assert response.json()["message"] == "User registered successfully"

def test_login_success():
    # Successful login
    response = client.post("/login", 
        data={"username": TEST_USER["username"], 
              "password": TEST_USER["password"]})
    assert response.status_code == 200
    assert "token" in response.json()

def test_login_failure():
    # Failed login
    response = client.post("/login", 
        data={"username": "wrong", "password": "wrong"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect username or password"

def test_protected_endpoint():
    # Get token first
    login_response = client.post("/login", 
        data={"username": TEST_USER["username"], 
              "password": TEST_USER["password"]})
    token = login_response.json()["token"]
    
    # Access protected endpoint
    response = client.post("/chat", 
        json={"user_input": "test message"},
        headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "ai_response" in response.json()

def test_emotional_response():
    login_response = client.post("/login", 
        data={"username": TEST_USER["username"], 
              "password": TEST_USER["password"]})
    token = login_response.json()["token"]
    
    # Angry message
    angry_response = client.post("/chat", 
        json={"user_input": "I'm furious about this!"},
        headers={"Authorization": f"Bearer {token}"})
    assert "calm" in angry_response.json()["ai_response"].lower()
    
    # Happy message
    happy_response = client.post("/chat", 
        json={"user_input": "I'm so excited!"},
        headers={"Authorization": f"Bearer {token}"})
    assert any(word in happy_response.json()["ai_response"].lower() 
              for word in ["great", "excited", "wonderful"])

def test_ethical_monitoring():
    login_response = client.post("/login", 
        data={"username": TEST_USER["username"], 
              "password": TEST_USER["password"]})
    token = login_response.json()["token"]
    
    # Test prohibited content
    response = client.post("/chat", 
        json={"user_input": "I want to do something illegal"},
        headers={"Authorization": f"Bearer {token}"})
    assert response.json()["ethical_check"]["risk_score"] > 0
    assert response.json()["ethical_check"]["needs_review"] == True

def test_chat_history():
    login_response = client.post("/login", 
        data={"username": TEST_USER["username"], 
              "password": TEST_USER["password"]})
    token = login_response.json()["token"]
    
    # Send multiple messages
    for msg in ["test1", "test2", "test3"]:
        client.post("/chat", 
            json={"user_input": msg},
            headers={"Authorization": f"Bearer {token}"})
    
    # Get history
    history_response = client.get("/history",
        headers={"Authorization": f"Bearer {token}"})
    assert len(history_response.json()["history"]) >= 3
