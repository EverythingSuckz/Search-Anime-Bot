import os
import asyncio
import requests
from AnimeBot import AnimeBot
from telethon import events, Button
from ..helpers.search import shorten, anime_query, GRAPHQL
from ..helpers.other import format_results, conv_to_jpeg

import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)


@AnimeBot.on(events.NewMessage(incoming=True, pattern='/anime ?(.*)'))
async def anime(event):
    input_str = event.pattern_match.group(1)
    ing = await AnimeBot.send_message(event.chat_id, f"__Searching for__ `{input_str}` __in Anilist__")
    variables = {'search': input_str}
    json = requests.post(GRAPHQL, json={'query': anime_query, 'variables': variables}).json()['data'].get('Media', None)
    if json:
        msg, info, trailer, image = format_results(json)
        if trailer:
            buttons =[
                [
                    Button.url("More Info", url=info),
                    Button.url("Trailer 🎬", url=trailer)
                ]
            ]
        else:
           buttons =[
                [
                    Button.url("More Info", url=info)
                ]
            ]
        if image:
            try:
                namae = conv_to_jpeg(image)
                await AnimeBot.send_file(event.chat_id, namae, caption=msg, buttons=buttons, reply_to=event.id, force_document=False)
                await ing.delete()
                os.remove(namae)
            except:
                msg += f" [\u2063]({image})"
                await ing.edit(msg, buttons=buttons)