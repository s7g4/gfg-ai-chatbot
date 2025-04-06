from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime

class UserRegister(BaseModel):
    username: constr(min_length=3, max_length=20)
    password: constr(min_length=8)

class EmotionAnalysisRequest(BaseModel):
    text: constr(min_length=1, max_length=500)

class VoiceAnalysisRequest(BaseModel):
    audio_data: str  # Base64 encoded audio
    sample_rate: Optional[int] = 16000

class ChatInput(BaseModel):
    message: constr(min_length=1, max_length=500)

class AnalyticsTimeRange(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
