# Career Scout Telegram

Telegram bot for monitoring job vacancy channels. Automatically filters and forwards relevant vacancies based on keywords.

## Features
- Real-time vacancy monitoring in multiple channels
- Keyword-based filtering with position matching
- Stop-words to exclude irrelevant messages
- Message deduplication using cache
- Customizable monitoring intervals
- Automatic cleanup of old cache entries
- Formatted vacancy notifications
- Real-time log monitoring

## Requirements
- Python 3.8 or higher
- Telegram API credentials:
  - API_ID and API_HASH from https://my.telegram.org
  - Telegram channel or group for monitoring
  - Target channel ID for notifications (Use @userinfobot to get ID)
- Internet connection
- Unix-like OS or Windows
- Storage for cache and logs

## Quick Start Guide

1. Get Telegram API credentials:
   - Go to https://my.telegram.org
   - Create an application
   - Save API_ID and API_HASH
   - Create a channel for notifications
   - Forward message from target channel to @userinfobot to get channel ID

2. Setup environment:
```bash
# Clone and setup
git clone https://github.com/miktaba/career-scout-telegram.git
cd career-scout-telegram

# Create directories
mkdir -p data/cache logs

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

## Configuration

1. Create configuration files:
```bash
cp .env.example .env
cp config/channels.yaml.example config/channels.yaml
```

2. Update `.env` with your Telegram credentials:
```env
TELEGRAM_API_ID=your_api_id_here
TELEGRAM_API_HASH=your_api_hash_here
CHANNEL_ID=your_channel_id_here
```

3. Configure monitoring in `channels.yaml`:
```yaml
settings:
  cache:
    file: "data/cache/messages_cache.json"  # Cache location
    size: 5000                              # Max cached messages
    ttl: 604800                             # Cache TTL (7 days)
  
  parser:
    days_to_parse: 2                        # Message history depth
    max_retries: 3                          # Retry attempts
    request_delay: 1                        # Anti-flood delay
    timezone: "UTC"                         # Time zone
    log_level: "INFO"                       # Log verbosity
    log_file: "logs/parser.log"            # Log location
    pause_minutes: 10                       # Cycle interval

channels:
  job_channels:
    - id: "@channel_name"                   # Channel to monitor

keywords:
  positions:                                # Keywords to match
    - "ios developer"
    - "ios engineer"
  
  stop_words:                               # Words to exclude
    - "resume"
    - "looking for"
```

## Available Commands

1. Parser control:
```bash
# Start parser
python -m src.parser

# Stop parser gracefully
Ctrl+C
```

2. Monitoring:
```bash
# Watch logs in real-time
python -m src.commands.watch_logs

# Clear message cache
python -m src.commands.clear_cache
```

3. Development:
```bash
# Run tests
pytest

# Check coverage
pytest --cov=src tests/
```

## Project Structure
```
career-scout-telegram/
├── config/                 # Configuration files
│   ├── channels.yaml      # Parser configuration
│   └── channels.yaml.example
├── data/
│   └── cache/            # Cache storage
├── logs/                 # Log files
├── src/                  # Source code
│   ├── commands/        # CLI utilities
│   │   ├── watch_logs.py
│   │   └── clear_cache.py
│   ├── cache.py        # Cache management
│   ├── config.py       # Config loading
│   ├── filters.py      # Message filtering
│   ├── formatter.py    # Message formatting
│   └── parser.py       # Main parser logic
├── tests/               # Test suite
├── .env                # Credentials
├── .gitignore         # Git ignore rules
├── README.md          # This file
├── requirements.txt   # Dependencies
└── setup.py          # Package setup
```

## Updates and Maintenance

1. Update repository:
```bash
git pull origin main
pip install -r requirements.txt
```

2. Clean up:
```bash
# Clear cache
python -m src.commands.clear_cache

# Remove old logs
rm logs/*.log
```

3. Backup:
```bash
# Backup configuration
cp config/channels.yaml config/channels.yaml.backup
cp .env .env.backup
```

## Troubleshooting

1. Cache issues:
   - Clear cache using `python -m src.commands.clear_cache`
   - Check cache file permissions
   - Verify cache configuration in channels.yaml

2. Connection errors:
   - Check internet connection
   - Verify Telegram credentials
   - Ensure channel IDs are correct
   - Check request_delay setting

3. Message filtering:
   - Review keywords configuration
   - Check stop_words list
   - Enable DEBUG logging for more details

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

MikTaba

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
