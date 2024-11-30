import os
import time
from pathlib import Path
from src.config import config

def watch_logs():
    log_file = Path(config.LOG_FILE)
    if not log_file.exists():
        print(f"Log file not found at: {log_file}")
        return

    print("Watching logs in real-time. Press Ctrl+C to stop.")
    try:
        with open(log_file, 'r') as f:
            # Go to the end of file
            f.seek(0, 2)
            while True:
                line = f.readline()
                if line:
                    print(line, end='')
                time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopped watching logs")

if __name__ == "__main__":
    watch_logs() 