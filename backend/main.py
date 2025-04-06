import sys
from fastapi import FastAPI, Depends, HTTPException, status, Body, Request, Response
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from models import (
    UserRegister,
    EmotionAnalysisRequest, 
    VoiceAnalysisRequest,
    ChatInput,
    AnalyticsTimeRange
)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from pymongo import MongoClient
from datetime import datetime, timedelta
import bcrypt
from dotenv import load_dotenv
import os
import numpy as np
import soundfile as sf
import librosa

load_dotenv()

app = FastAPI(middleware=[
    Middleware(CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
])

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Use test database when running pytest
if "pytest" in sys.modules:
    from mongomock import MongoClient
    client = MongoClient()
    db = client.test_db
    users = db.users
    users.insert_one({
        "username": os.getenv("TEST_USERNAME"),
        "password": bcrypt.hashpw(os.getenv("TEST_PASSWORD").encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    })
else:
    from mongomock import MongoClient
    client = MongoClient()
    db = client.test_db
    users = db.users
    # Create test user
    users.insert_one({
        "username": "test",
        "password": bcrypt.hashpw("secret".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    })

@app.post("/register")
async def register(user: UserRegister):
    existing_user = users.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    users.insert_one({"username": user.username, "password": hashed_password})
    return {"message": "User registered successfully"}

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users.find_one({"username": form_data.username})
    if not user or not bcrypt.checkpw(form_data.password.encode('utf-8'), user["password"].encode('utf-8')):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.encode(
        {"sub": form_data.username, "exp": datetime.utcnow() + access_token_expires},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/emotion")
async def emotion_analysis(request: EmotionAnalysisRequest, token: str = Depends(oauth2_scheme)):
    # Mock implementation for testing
    return {"emotion": "happy", "confidence": 0.95}

@app.post("/chat")
async def chat(input: ChatInput, token: str = Depends(oauth2_scheme)):
    # Mock implementation for testing
    return {"response": "This is a mock response"}

@app.post("/voice")
async def voice_analysis(request: VoiceAnalysisRequest, token: str = Depends(oauth2_scheme)):
    # Mock implementation for testing
    return {"emotion": "neutral", "confidence": 0.85}
