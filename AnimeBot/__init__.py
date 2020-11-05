import os
from telethon import TelegramClient, events
import logging

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

API_ID = os.environ.get("API_ID", None)
API_HASH = os.environ.get("API_HASH", None)
BOT_TOKEN = os.environ.get("BOT_TOKEN", None)

AnimeBot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)