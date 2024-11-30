from typing import Dict, List
from src.config import config

class MessageFilter:
    def __init__(self):
        keywords = config.get_keywords()
        self.positions = [pos.lower() for pos in keywords['positions']]
        self.stop_words = [word.lower() for word in keywords['stop_words']]

    def is_relevant(self, text: str) -> bool:
        """Check if text matches search criteria"""
        text = text.lower()
        
        # Check stop words
        if any(word in text for word in self.stop_words):
            return False
            
        # Check position keywords
        has_position = any(pos in text for pos in self.positions)
        
        return has_position

    def extract_keywords(self, text: str) -> Dict[str, List[str]]:
        """Extract found keywords from text"""
        text = text.lower()
        found_keywords = {
            'positions': [pos for pos in self.positions if pos in text]
        }
        return found_keywords 