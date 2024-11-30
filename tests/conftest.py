import pytest
from pathlib import Path
import json
from datetime import datetime
import pytz

@pytest.fixture
def sample_message_text():
    return """
    Looking for iOS Developer
    
    Requirements:
    - 3+ years of experience
    - Strong knowledge of Swift
    - Experience with UIKit and SwiftUI
    
    Location: Remote
    Contact: @hr_manager
    """

@pytest.fixture
def sample_keywords():
    return {
        'positions': ['ios developer', 'ios engineer']
    }

@pytest.fixture
def temp_cache_file(tmp_path):
    cache_file = tmp_path / "test_cache.json"
    cache_data = {
        "1234_5678": int(datetime.now(pytz.UTC).timestamp())
    }
    with open(cache_file, 'w') as f:
        json.dump(cache_data, f)
    return cache_file 