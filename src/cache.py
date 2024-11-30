import json
import time
from pathlib import Path
from typing import Dict, Optional
from src.config import config

class MessageCache:
    def __init__(self):
        self.cache_file = config.CACHE_FILE
        self.cache_size = config.CACHE_SIZE
        self.cache_ttl = config.CACHE_TTL
        self.cache: Dict = self._load_cache()

    def _load_cache(self) -> Dict:
        """Load cache from file or return empty dict if file doesn't exist"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def _save_cache(self):
        """Save cache to file"""
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f)

    def add_message(self, message_id: int, channel_id: int):
        """Add message to cache with current timestamp"""
        current_time = int(time.time())
        self.cache[f"{channel_id}_{message_id}"] = current_time
        
        # Clean old entries
        self._cleanup()
        self._save_cache()

    def message_exists(self, message_id: int, channel_id: int) -> bool:
        """Check if message exists in cache and not expired"""
        key = f"{channel_id}_{message_id}"
        if key in self.cache:
            timestamp = self.cache[key]
            if time.time() - timestamp < self.cache_ttl:
                return True
            del self.cache[key]
        return False

    def _cleanup(self):
        """Remove expired entries and limit cache size"""
        current_time = time.time()
        # Remove expired entries
        self.cache = {
            k: v for k, v in self.cache.items()
            if current_time - v < self.cache_ttl
        }
        
        # If cache is still too large, remove oldest entries
        if len(self.cache) > self.cache_size:
            sorted_items = sorted(self.cache.items(), key=lambda x: x[1])
            self.cache = dict(sorted_items[-self.cache_size:]) 