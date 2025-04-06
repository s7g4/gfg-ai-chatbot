from typing import Dict
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

class EthicalMonitor:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGO_URI"))
        self.db = self.client[os.getenv("DATABASE_NAME")]
        self.flagged_interactions = self.db.flagged_interactions
        self.ethical_guidelines = {
            "bias": ["gender", "race", "age", "religion"],
            "sensitive_topics": ["politics", "health", "finances"],
            "prohibited_content": ["hate speech", "violence", "illegal activities"]
        }
        
    def check_response(self, username: str, user_input: str, ai_response: str) -> Dict:
        """Check response against ethical guidelines"""
        analysis = {
            "flags": [],
            "risk_score": 0,
            "needs_review": False
        }
        
        # Check for biased language
        analysis.update(self._check_bias(ai_response))
        
        # Check for sensitive topics
        analysis.update(self._check_sensitive_topics(user_input))
        
        # Check for prohibited content
        analysis.update(self._check_prohibited_content(user_input))
        
        # Log flagged interactions
        if analysis["flags"]:
            self._log_flagged_interaction(username, user_input, ai_response, analysis)
            analysis["needs_review"] = True
            
        return analysis
    
    def _check_bias(self, text: str) -> Dict:
        """Check for biased language in responses"""
        results = {"flags": [], "risk_score": 0}
        text_lower = text.lower()
        
        for bias_term in self.ethical_guidelines["bias"]:
            if bias_term in text_lower:
                results["flags"].append(f"potential_bias:{bias_term}")
                results["risk_score"] += 1
                
        return results
    
    def _check_sensitive_topics(self, text: str) -> Dict:
        """Check for sensitive topics in user input"""
        results = {"flags": [], "risk_score": 0}
        text_lower = text.lower()
        
        for topic in self.ethical_guidelines["sensitive_topics"]:
            if topic in text_lower:
                results["flags"].append(f"sensitive_topic:{topic}")
                results["risk_score"] += 0.5
                
        return results
    
    def _check_prohibited_content(self, text: str) -> Dict:
        """Check for prohibited content with more sophisticated detection"""
        results = {"flags": [], "risk_score": 0}
        text_lower = text.lower()
        
        prohibited_patterns = {
            "illegal activities": ["illegal", "against the law", "criminal", 
                                 "break the law", "law breaking", "something illegal"],
            "violence": ["violence", "hurt", "attack", "fight", "harm", "kill"],
            "hate speech": ["hate", "racist", "sexist", "bigot", "prejudice"]
        }
        
        for content_type, patterns in prohibited_patterns.items():
            for pattern in patterns:
                if pattern in text_lower:
                    results["flags"].append(f"prohibited_content:{content_type}")
                    results["risk_score"] += 2
                    break  # Only flag once per content type
                    
        return results
    
    def _log_flagged_interaction(self, username: str, user_input: str, 
                               ai_response: str, analysis: Dict) -> None:
        """Log flagged interactions for human review"""
        self.flagged_interactions.insert_one({
            "username": username,
            "user_input": user_input,
            "ai_response": ai_response,
            "flags": analysis["flags"],
            "risk_score": analysis["risk_score"],
            "timestamp": datetime.utcnow(),
            "reviewed": False
        })
