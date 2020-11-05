import os
import asyncio
import requests
from AnimeBot import AnimeBot
from telethon import events, Button
from ..helpers.search import shorten, anime_query, GRAPHQL

import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

@AnimeBot.on(events.NewMessage(incoming=True, pattern='/anime ?(.*)'))
async def anime(event):
    input_str = event.pattern_match.group(1)
    ing = await AnimeBot.send_message(event.chat_id, f"__Searching for__ `{input_str}` __in Anilist__")
    variables = {'search': input_str}
    json = requests.post(GRAPHQL, json={'query': anime_query, 'variables': variables}).json()[
        'data'].get('Media', None)
    if json:
        msg = f"**{json['title']['romaji']}**(`{json['title']['native']}`)\n**Type**: {json['format']}\n**Status**: {json['status']}\n**Episodes**: {json.get('episodes', 'N/A')}\n**Duration**: {json.get('duration', 'N/A')} Per Ep.\n**Score**: {json['averageScore']}\n**Genres**: `"
        for x in json['genres']:
            msg += f"{x}, "
        msg = msg[:-2] + '`\n'
        msg += "**Studios**: `"
        for x in json['studios']['nodes']:
            msg += f"{x['name']}, "
        msg = msg[:-2] + '`\n'
        info = json.get('siteUrl')
        trailer = json.get('trailer', None)
        if trailer:
            trailer_id = trailer.get('id', None)
            site = trailer.get('site', None)
            if site == "youtube":
                trailer = 'https://youtu.be/' + trailer_id
        description = json.get(
            'description', 'N/A').replace('<i>', '').replace('</i>', '').replace('<br>', '')
        msg += shorten(description, info)
        image = info.replace('anilist.co/anime/', 'img.anili.st/media/')
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
                await AnimeBot.send_file(event.chat_id, image, caption=msg, buttons=buttons, reply_to=event.id)
                await ing.delete()
                file = open("results.txt", "w+")
                file.write(str(json))
                file.close()
                await AnimeBot.send_file(event.chat_id, "results.txt")
                await os.remove("results.txt")
            except:
                msg += f" [〽️]({image})"
                await ing.edit(msg)
        else:
            await ing.edit(msg)