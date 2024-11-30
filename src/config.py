import os
from pathlib import Path
from typing import Dict, List
import yaml
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent
CONFIG_DIR = BASE_DIR / "config"
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = DATA_DIR / "cache"
LOGS_DIR = BASE_DIR / "logs"

# Create required directories
CACHE_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

class Config:
    def __init__(self):
        self._config = self._load_config()
        
    def _load_config(self) -> Dict:
        """Loads configuration from YAML file"""
        config_file = CONFIG_DIR / "channels.yaml"
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    # Telegram credentials from .env
    API_ID: int = int(os.getenv("TELEGRAM_API_ID"))
    API_HASH: str = os.getenv("TELEGRAM_API_HASH")
    CHANNEL_ID: int = int(os.getenv("CHANNEL_ID"))
    
    # Cache settings from YAML
    @property
    def CACHE_FILE(self) -> Path:
        return Path(self._config['settings']['cache']['file'])
    
    @property
    def CACHE_SIZE(self) -> int:
        return self._config['settings']['cache']['size']
    
    @property
    def CACHE_TTL(self) -> int:
        return self._config['settings']['cache']['ttl']
    
    # Parser settings from YAML
    @property
    def DAYS_TO_PARSE(self) -> int:
        return self._config['settings']['parser']['days_to_parse']
    
    @property
    def MAX_RETRIES(self) -> int:
        return self._config['settings']['parser']['max_retries']
    
    @property
    def REQUEST_DELAY(self) -> float:
        return self._config['settings']['parser']['request_delay']
    
    @property
    def TIMEZONE(self) -> str:
        return self._config['settings']['parser']['timezone']
    
    @property
    def LOG_LEVEL(self) -> str:
        return self._config['settings']['parser']['log_level']
    
    @property
    def LOG_FILE(self) -> Path:
        return Path(self._config['settings']['parser']['log_file'])
    
    # Channel and keyword settings
    def get_channels(self) -> List[Dict]:
        """Returns list of channels"""
        return self._config['channels']['job_channels']
    
    def get_keywords(self) -> Dict[str, List[str]]:
        """Returns keyword settings"""
        return self._config['keywords']
    
    @property
    def PAUSE_MINUTES(self) -> int:
        return self._config['settings']['parser']['pause_minutes']

# Create global config instance
config = Config() 