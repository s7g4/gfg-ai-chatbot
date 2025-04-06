from transformers import pipeline
import torch
from typing import Dict, List, Optional
from pydantic import BaseModel

class EmotionAnalysisResult(BaseModel):
    emotion: str
    confidence: float
    suggested_response_tone: str
    emotion_scores: Dict[str, float]

class EmotionAnalyzer:
    def __init__(self):
        # Load pre-trained emotion analysis model
        self.model = pipeline(
            "text-classification",
            model="SamLowe/roberta-base-go_emotions",
            device=0 if torch.cuda.is_available() else -1,
            return_all_scores=True
        )
        self.emotion_mapping = {
            "anger": "angry",
            "disappointment": "frustrated",
            "neutral": "neutral",
            "joy": "happy",
            "surprise": "excited",
            "sadness": "sad",
            "fear": "anxious"
        }
        
    def analyze_text(self, text: str) -> EmotionAnalysisResult:
        """Analyze text for emotional tone using transformer model"""
        results = self.model(text)
        
        # Process all emotion scores
        emotion_scores = {
            self._map_emotion(entry['label']): entry['score'] 
            for entry in results[0]
        }
        
        # Get dominant emotion
        dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])
        
        return EmotionAnalysisResult(
            emotion=dominant_emotion[0],
            confidence=dominant_emotion[1],
            suggested_response_tone=self._get_response_tone(dominant_emotion[0]),
            emotion_scores=emotion_scores
        )
    
    def _map_emotion(self, emotion_label: str) -> str:
        """Map model-specific labels to our standard emotion set"""
        return self.emotion_mapping.get(
            emotion_label.split('_')[-1].lower(),
            "neutral"
        )
    
    def _get_response_tone(self, emotion: str) -> str:
        """Get appropriate response tone based on user's emotion"""
        tone_mapping = {
            "angry": "calm, patient and understanding",
            "frustrated": "calm, patient and supportive",
            "neutral": "professional and helpful",
            "happy": "friendly and enthusiastic",
            "excited": "energetic and encouraging",
            "sad": "compassionate and supportive",
            "anxious": "reassuring and clear"
        }
        return tone_mapping.get(emotion, "professional")
