import pytest
from datetime import datetime
import pytz
from src.formatter import MessageFormatter

def test_format_message(sample_message_text, sample_keywords, monkeypatch):
    class MockConfig:
        TIMEZONE = 'UTC'
    
    monkeypatch.setattr('src.formatter.config', MockConfig())
    
    formatter = MessageFormatter()
    now = datetime.now(pytz.UTC)
    
    message = formatter.format_message(
        original_text=sample_message_text,
        channel_name="@test_channel",
        message_url="https://t.me/c/123/456",
        keywords=sample_keywords,
        published_date=now
    )
    
    assert "New vacancy!" in message
    assert "@test_channel" in message
    assert "ios developer" in message
    assert "https://t.me/c/123/456" in message 