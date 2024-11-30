import pytest
from src.filters import MessageFilter

def test_is_relevant(sample_message_text, monkeypatch):
    class MockConfig:
        @staticmethod
        def get_keywords():
            return {
                'positions': ['ios developer', 'ios engineer'],
                'stop_words': ['searching', 'resume']
            }
    
    monkeypatch.setattr('src.filters.config', MockConfig())
    
    filter = MessageFilter()
    
    # Test relevant message
    assert filter.is_relevant(sample_message_text) == True
    
    # Test irrelevant message
    assert filter.is_relevant("Python developer needed") == False

def test_extract_keywords(sample_message_text, monkeypatch):
    class MockConfig:
        @staticmethod
        def get_keywords():
            return {
                'positions': ['ios developer', 'ios engineer'],
                'stop_words': ['searching', 'resume']
            }
    
    monkeypatch.setattr('src.filters.config', MockConfig())
    
    filter = MessageFilter()
    keywords = filter.extract_keywords(sample_message_text)
    
    assert 'positions' in keywords
    assert 'ios developer' in keywords['positions'] 