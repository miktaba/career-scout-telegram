from typing import Dict, List
from datetime import datetime
import pytz
from src.config import config

class MessageFormatter:
    def __init__(self):
        self.timezone = pytz.timezone(config.TIMEZONE)

    def format_message(self, 
                      original_text: str,
                      channel_name: str,
                      message_url: str,
                      keywords: Dict[str, List[str]],
                      published_date: datetime) -> str:
        """Format message for sending"""
        # Convert time to target timezone
        local_date = published_date.astimezone(self.timezone)
        date_str = local_date.strftime("%Y-%m-%d %H:%M")
        
        # Format found keywords
        positions = ", ".join(keywords['positions'])
        
        # Create message in markdown format
        message = (
            f"🔍 **New vacancy!**\n\n"
            f"📅 Date: {date_str}\n"
            f"📢 Channel: {channel_name}\n"
            f"💼 Position: {positions}\n\n"
            f"📝 **Description:**\n"
            f"{original_text[:1000]}...\n\n"  # Truncate long text
            f"🔗 [Original message]({message_url})"
        )
        
        return message 