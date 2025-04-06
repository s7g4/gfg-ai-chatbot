from typing import Dict, List
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

class DigitalTwin:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGO_URI"))
        self.db = self.client[os.getenv("DATABASE_NAME")]
        self.user_profiles = self.db.user_profiles
        self.conversation_history = self.db.conversation_history
        
    def get_user_profile(self, username: str) -> Dict:
        """Get or create user profile"""
        profile = self.user_profiles.find_one({"username": username})
        if not profile:
            profile = {
                "username": username,
                "preferences": {},
                "interaction_style": "neutral",
                "issue_history": [],
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            self.user_profiles.insert_one(profile)
        return profile
    
    def update_profile(self, username: str, interaction_data: Dict) -> None:
        """Update user profile based on interaction"""
        updates = {
            "interaction_style": interaction_data.get("tone", "neutral"),
            "updated_at": datetime.utcnow(),
            "last_emotion": interaction_data.get("emotion_scores", {})
        }
        
        # Track recurring issues
        if "issue" in interaction_data:
            self.user_profiles.update_one(
                {"username": username},
                {"$addToSet": {"issue_history": interaction_data["issue"]}}
            )
            
        # Update emotion history
        self.user_profiles.update_one(
            {"username": username},
            {
                "$set": updates,
                "$push": {
                    "emotion_history": {
                        "timestamp": datetime.utcnow(),
                        "emotion": interaction_data.get("tone"),
                        "scores": interaction_data.get("emotion_scores", {})
                    }
                }
            }
        )
    
    def get_personalized_response(self, username: str, base_response: str) -> str:
        """Personalize a response based on user's profile"""
        profile = self.get_user_profile(username)
        
        # Get emotion trends
        emotion_trend = self._get_emotion_trend(username)
        
        # Add personalization based on current and historical emotions
        if profile["interaction_style"] == "angry":
            if emotion_trend.get("angry", 0) > 0.3:
                return f"I can see this has been really frustrating for you. {base_response}"
            return f"I understand this has been frustrating. {base_response}"
        elif profile["interaction_style"] == "happy":
            if emotion_trend.get("happy", 0) > 0.5:
                return f"You seem particularly happy today! {base_response}"
            return f"Great to chat with you again! {base_response}"
        elif profile["interaction_style"] == "anxious":
            return f"I want to reassure you that {base_response.lower()}"
        
        # Check for recurring issues
        if len(profile.get("issue_history", [])) > 2:
            recurring_issue = max(set(profile["issue_history"]), 
                                key=profile["issue_history"].count)
            return f"Regarding your concern about {recurring_issue}, {base_response}"
            
        return base_response
    
    def _get_emotion_trend(self, username: str) -> Dict[str, float]:
        """Calculate emotion trends from recent history"""
        history = list(self.user_profiles.aggregate([
            {"$match": {"username": username}},
            {"$unwind": "$emotion_history"},
            {"$sort": {"emotion_history.timestamp": -1}},
            {"$limit": 5},
            {"$group": {
                "_id": None,
                "avg_scores": {
                    "$avg": {
                        "$map": {
                            "input": {"$objectToArray": "$emotion_history.scores"},
                            "as": "score",
                            "in": "$$score.v"
                        }
                    }
                }
            }}
        ]))
        
        return history[0]["avg_scores"] if history else {}
    
    def log_interaction(self, username: str, message: str, response: str) -> None:
        """Log conversation history"""
        self.conversation_history.insert_one({
            "username": username,
            "user_message": message,
            "ai_response": response,
            "timestamp": datetime.utcnow()
        })
