import re
import random
from AnimeBot import AnimeBot
from telethon import events
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import KeyboardButtonCallback

@AnimeBot.on(events.NewMessage(pattern="^/start ?(.*)"))
async def start(event):
    vent = event.chat_id
    full = await AnimeBot.GetFullUserRequest(event.from_id)
    await AnimeBot.send_message(event.chat_id, f"Hi [{(full.user.first_name)}](tg://user?id={event.from_id}),\nThis bot in Test Stage!",
        buttons=[
            [
                KeyboardButtonCallback(text="Help", data="chelp")
            ]
        ])

@AnimeBot.on(events.callbackquery.CallbackQuery(data=re.compile(b"help")))
async def chelp(event):
    await event.edit("Help",
        buttons=[
            [
                KeyboardButtonCallback(text="Test Button", data="test")
            ]
        ]
    )

EVERYTHINGSUCKS = [
    "...no",
    "This is a Test",
    "You've Clicked this Button"
]

@AnimeBot.on(events.callbackquery.CallbackQuery(data=re.compile(b"test")))
async def thissucks(event):
        bruh = random.choice(EVERYTHINGSUCKS)
        await event.answer(bruh, alert=True)