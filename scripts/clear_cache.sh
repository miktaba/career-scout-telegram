#!/bin/bash

# Check if cache file exists
CACHE_FILE="data/cache/messages_cache.json"
if [ ! -f "$CACHE_FILE" ]; then
    echo "Cache file not found at: $CACHE_FILE"
    exit 1
fi

# Remove cache file
rm "$CACHE_FILE"
echo "Cache cleared successfully" 