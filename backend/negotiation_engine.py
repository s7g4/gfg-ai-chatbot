from typing import Dict, List
import random
from enum import Enum

class NegotiationStrategy(Enum):
    COLLABORATIVE = "collaborative"
    COMPETITIVE = "competitive"
    ACCOMMODATING = "accommodating"
    COMPROMISING = "compromising"
    AVOIDING = "avoiding"

class NegotiationEngine:
    def __init__(self):
        self.strategy_weights = {
            NegotiationStrategy.COLLABORATIVE: 0.4,
            NegotiationStrategy.COMPETITIVE: 0.1,
            NegotiationStrategy.ACCOMMODATING: 0.3,
            NegotiationStrategy.COMPROMISING: 0.2,
            NegotiationStrategy.AVOIDING: 0.0
        }
        
    def determine_strategy(self, emotion_data: Dict) -> NegotiationStrategy:
        """Determine negotiation strategy based on user's emotional state"""
        tone = emotion_data.get('tone', 'neutral')
        
        # Adjust strategy weights based on emotion
        if tone == "angry":
            # Force accommodating strategy for angry messages
            return NegotiationStrategy.ACCOMMODATING
        elif tone == "frustrated":
            self.strategy_weights[NegotiationStrategy.COMPROMISING] = 0.4
            self.strategy_weights[NegotiationStrategy.COLLABORATIVE] = 0.4
        elif tone == "positive" or tone == "excited":
            self.strategy_weights[NegotiationStrategy.COLLABORATIVE] = 1.0
            self.strategy_weights[NegotiationStrategy.ACCOMMODATING] = 0.0
            
        # Select strategy based on weighted probabilities
        strategies = list(self.strategy_weights.keys())
        weights = list(self.strategy_weights.values())
        return random.choices(strategies, weights=weights, k=1)[0]
    
    def generate_response(self, strategy: NegotiationStrategy, user_input: str) -> str:
        """Generate negotiation response based on selected strategy"""
        response_templates = {
            NegotiationStrategy.COLLABORATIVE: [
                "I understand your concern about {issue}. Let's work together to find a great solution!",
                "I'm excited to explore wonderful options that work for both of us!",
                "This is great - let's collaborate to find the best approach.",
                "I'm happy to help with this! Let's find a fantastic solution together.",
                "Wonderful! I'm excited we can work on this together."
            ],
            NegotiationStrategy.COMPETITIVE: [
                "Our policy clearly states that {issue} cannot be accommodated.",
                "I'm afraid we cannot agree to that request."
            ],
            NegotiationStrategy.ACCOMMODATING: [
                "I completely understand your frustration. Let's stay calm - I'm here to help resolve this.",
                "I hear how upset you are. Please stay calm with me as we work through this together.",
                "I appreciate you sharing this. Let's remain calm and find the best solution for you."
            ],
            NegotiationStrategy.COMPROMISING: [
                "While we can't do exactly what you're asking, perhaps we could meet halfway on {issue}?",
                "I can offer a partial solution that might work for both of us."
            ]
        }
        
        # Extract issue from user input
        issue = self._extract_issue(user_input)
        
        if strategy == NegotiationStrategy.AVOIDING:
            return "Let's discuss this later when we have more options available."
            
        template = random.choice(response_templates[strategy])
        return template.format(issue=issue)
    
    def _extract_issue(self, text: str) -> str:
        """Simple issue extraction from text"""
        keywords = ["refund", "price", "service", "product", "delivery", "quality"]
        for word in keywords:
            if word in text.lower():
                return word
        return "this matter"
