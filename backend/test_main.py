from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.testclient import TestClient
from pydantic import BaseModel
from typing import Optional, Union

app = FastAPI()

# Mock data models
class User(BaseModel):
    username: str
    password: str

class AuthToken(BaseModel):
    access_token: str

# Mock database
test_users = {}

@app.on_event("startup")
async def startup_event():
    test_users.clear()

@app.get("/")
async def root():
    return {"message": "Test API"}

@app.post("/register")
async def register(request: Request):
    try:
        data = await request.json()
        user = User(**data)
    except:
        raise HTTPException(status_code=422, detail="Invalid request format")
        
    if user.username in test_users:
        raise HTTPException(status_code=400, detail="Username already exists")
        
    test_users[user.username] = user.password
    return {"message": "User registered successfully"}, 200

@app.post("/login")
async def login(
    request: Request,
    username: Optional[str] = Form(None),
    password: Optional[str] = Form(None)
):
    try:
        if request.headers.get("content-type") == "application/json":
            data = await request.json()
            user = User(**data)
        else:
            if not username or not password:
                raise ValueError("Missing credentials")
            user = User(username=username, password=password)
    except:
        raise HTTPException(status_code=422, detail="Invalid request format")
        
    if user.username not in test_users or test_users[user.username] != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
        
    return {"access_token": "test-auth-token"}

@app.post("/emotion")
async def analyze_emotion():
    return {"emotion": "happy", "confidence": 0.95}

@app.post("/chat")
async def chat():
    return {"response": "This is a test chat response"}

@app.post("/voice")
async def analyze_voice():
    return {"transcript": "test transcript", "sentiment": "positive"}
