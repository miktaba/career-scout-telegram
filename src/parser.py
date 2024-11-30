import asyncio
import signal
import sys
from datetime import datetime, timedelta
import pytz
from telethon import TelegramClient
from telethon.errors import FloodWaitError
from telethon.tl.types import Message

from src.config import config
from src.cache import MessageCache
from src.filters import MessageFilter
from src.formatter import MessageFormatter
from src.logger import logger

class TelegramParser:
    def __init__(self):
        self.client = TelegramClient('career_scout',
                                   config.API_ID,
                                   config.API_HASH)
        self.cache = MessageCache()
        self.filter = MessageFilter()
        self.formatter = MessageFormatter()
        self.target_channel = config.CHANNEL_ID
        self.is_running = True
        
    def stop_parser(self):
        """Stop parser gracefully"""
        logger.info("Stopping parser gracefully...")
        self.is_running = False
        
    async def shutdown(self, signal=None):
        """Cleanup and shutdown"""
        if signal:
            logger.info(f"Received exit signal {signal.name}...")
        
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        [task.cancel() for task in tasks]
        
        logger.info(f"Cancelling {len(tasks)} outstanding tasks")
        await asyncio.gather(*tasks, return_exceptions=True)
        logger.info("Stopping event loop...")
        asyncio.get_event_loop().stop()

    def _handle_exception(self, loop, context):
        msg = context.get("exception", context["message"])
        logger.error(f"Caught exception: {msg}")
        logger.info("Shutting down...")
        asyncio.create_task(self.shutdown())

    async def start(self):
        """Start Telegram client"""
        await self.client.start()
        
    async def stop(self):
        """Stop Telegram client"""
        await self.client.disconnect()
        
    def _get_message_url(self, channel_id: int, message_id: int) -> str:
        """Generate message URL"""
        return f"https://t.me/c/{str(channel_id)[4:]}/{message_id}"
        
    async def process_message(self, message: Message, channel_id: str):
        """Process single message"""
        if not message.text or not self.is_running:
            return
            
        # Check if message already processed
        if self.cache.message_exists(message.id, message.peer_id.channel_id):
            return
            
        # Check message relevance
        if not self.filter.is_relevant(message.text):
            return
            
        # Extract keywords
        keywords = self.filter.extract_keywords(message.text)
        logger.info(f"Found relevant message in {channel_id} with keywords: {keywords['positions']}")
        
        # Generate message URL
        message_url = self._get_message_url(message.peer_id.channel_id, message.id)
        
        # Format message
        formatted_message = self.formatter.format_message(
            original_text=message.text,
            channel_name=channel_id,
            message_url=message_url,
            keywords=keywords,
            published_date=message.date
        )
        
        try:
            if not self.is_running:
                return
                
            # Send message
            await self.client.send_message(
                self.target_channel,
                formatted_message,
                parse_mode='markdown',
                link_preview=False
            )
            
            # Add to cache
            self.cache.add_message(message.id, message.peer_id.channel_id)
            
            # Delay to avoid flood
            if self.is_running:
                await asyncio.sleep(config.REQUEST_DELAY)
            
        except FloodWaitError as e:
            logger.warning(f"Hit flood limit, waiting {e.seconds} seconds")
            if self.is_running:
                await asyncio.sleep(e.seconds)
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            
    async def process_channel(self, channel: dict):
        """Process all messages from channel"""
        if not self.is_running:
            return
            
        try:
            channel_id = channel['id']
            channel_entity = await self.client.get_entity(channel_id)
            
            # Define time range
            now = datetime.now(pytz.UTC)
            since_date = now - timedelta(days=config.DAYS_TO_PARSE)
            
            async for message in self.client.iter_messages(
                channel_entity,
                offset_date=since_date,
                reverse=True
            ):
                if not self.is_running:
                    break
                await self.process_message(message, channel_id)
                
        except Exception as e:
            logger.error(f"Error processing channel {channel_id}: {e}")
            
    async def run(self):
        """Run parser"""
        try:
            await self.start()
            
            while self.is_running:
                channels = config.get_channels()
                now = datetime.now(pytz.UTC)
                since_date = now - timedelta(days=config.DAYS_TO_PARSE)
                logger.info(f"Starting new scan cycle. Checking messages from {since_date} to {now}")
                
                for channel in channels:
                    if not self.is_running:
                        break
                    logger.info(f"Processing channel: {channel['id']}")
                    await self.process_channel(channel)
                    
                if self.is_running:
                    pause_seconds = config.PAUSE_MINUTES * 60
                    next_run = datetime.now() + timedelta(minutes=config.PAUSE_MINUTES)
                    logger.info(f"Finished processing all channels. Next run at: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
                    await asyncio.sleep(pause_seconds)
                
        finally:
            await self.stop()
            
def main():
    parser = TelegramParser()
    loop = asyncio.get_event_loop()
    
    # Set up exception handling
    loop.set_exception_handler(parser._handle_exception)
    
    # Set up signal handlers
    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(
            sig,
            lambda s=sig: asyncio.create_task(parser.shutdown(sig))
        )
    
    try:
        loop.run_until_complete(parser.run())
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        logger.info("Successfully shutdown the parser.")
        sys.exit(0)

if __name__ == "__main__":
    main() 