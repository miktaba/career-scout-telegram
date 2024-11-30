#!/bin/bash

# Check if log file exists
LOG_FILE="logs/parser.log"
if [ ! -f "$LOG_FILE" ]; then
    echo "Log file not found at: $LOG_FILE"
    exit 1
fi

# Watch logs in real-time
echo "Watching logs in real-time. Press Ctrl+C to stop."
tail -f "$LOG_FILE" 