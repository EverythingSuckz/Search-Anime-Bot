import time
from utils import t
from telethon import events
from datetime import datetime
from AnimeBot import AnimeBot, StartTime

@AnimeBot.on(events.NewMessage(pattern="^/ping"))
async def _(event):
    start = datetime.now()
    vent = event.chat_id
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    uptime = t((time.time() - StartTime))
    await AnimeBot.send_message(vent, f"🏓Ping speed: {ms}\n😵Uptime: {uptime}")