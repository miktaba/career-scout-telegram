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
  - Target channel ID for notifications
- Internet connection
- Unix-like OS or Windows

## Installation

1. Clone repository:
```bash
git clone https://github.com/yourusername/career-scout-telegram.git
cd career-scout-telegram
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
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

## Usage

1. Start the parser:
```bash
python -m src.parser
```

2. Watch logs in real-time:
```bash
python -m src.commands.watch_logs
```

3. Clear message cache:
```bash
python -m src.commands.clear_cache
```
3. Stop the parser:  Ctrl+C 

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

## Development

Run tests:
```bash
# Install test dependencies
pip install pytest pytest-cov pytest-asyncio

# Run tests
pytest

# Run with coverage
pytest --cov=src tests/
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
