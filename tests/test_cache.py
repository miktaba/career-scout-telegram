import pytest
import json
import time
from src.cache import MessageCache

def test_message_exists(temp_cache_file, monkeypatch):
    # Mock config
    class MockConfig:
        CACHE_FILE = temp_cache_file
        CACHE_SIZE = 1000
        CACHE_TTL = 3600
    
    monkeypatch.setattr('src.cache.config', MockConfig())
    
    cache = MessageCache()
    
    # Test existing message
    assert cache.message_exists(5678, 1234) == True
    
    # Test non-existing message
    assert cache.message_exists(9999, 9999) == False

def test_add_message(temp_cache_file, monkeypatch):
    class MockConfig:
        CACHE_FILE = temp_cache_file
        CACHE_SIZE = 1000
        CACHE_TTL = 3600
    
    monkeypatch.setattr('src.cache.config', MockConfig())
    
    cache = MessageCache()
    cache.add_message(1111, 2222)
    
    # Verify message was added
    with open(temp_cache_file, 'r') as f:
        data = json.load(f)
        assert "2222_1111" in data

def test_cleanup_old_messages(temp_cache_file, monkeypatch):
    # Create initial cache file with old message
    old_timestamp = int(time.time()) - 3600  # 1 hour ago
    initial_cache = {
        "1234_5678": old_timestamp
    }
    with open(temp_cache_file, 'w') as f:
        json.dump(initial_cache, f)

    class MockConfig:
        CACHE_FILE = temp_cache_file
        CACHE_SIZE = 1000
        CACHE_TTL = 1  # 1 second TTL
    
    monkeypatch.setattr('src.cache.config', MockConfig())
    
    # Initialize cache and run cleanup
    cache = MessageCache()
    cache._cleanup()
    
    # Save changes to file
    cache._save_cache()
    
    # Verify old messages were removed from file
    with open(temp_cache_file, 'r') as f:
        data = json.load(f)
        assert len(data) == 0