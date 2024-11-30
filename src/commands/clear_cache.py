from pathlib import Path
from src.config import config

def clear_cache():
    cache_file = Path(config.CACHE_FILE)
    if not cache_file.exists():
        print(f"Cache file not found at: {cache_file}")
        return

    cache_file.unlink()
    print("Cache cleared successfully")

if __name__ == "__main__":
    clear_cache() 