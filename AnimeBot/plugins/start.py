from AnimeBot import AnimeBot
from telethon import events

@AnimeBot.on(events.NewMessage(incoming=True, pattern='/start ?(.*)'))
async def anime(event):
    await AnimeBot.send_message(event.chat_id, f"__Working for Now__")