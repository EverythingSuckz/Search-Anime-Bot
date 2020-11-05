from AnimeBot import AnimeBot
from telethon import events, Button
from ..helpers.search import shorten, anime_query, GRAPHQL
import requests
import telethon
from telethon.tl.types import BotInlineResult, InputBotInlineMessageMediaAuto, DocumentAttributeImageSize, InputWebDocument, InputBotInlineResult
from telethon.tl.functions.messages import SetInlineBotResultsRequest


@AnimeBot.on(events.InlineQuery(pattern='anime ?(.*)'))
async def inline_anime(event):
    builder = event.builder
    query = event.pattern_match.group(1)
    variables = {'search': query}
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
        results = builder.photo(
            file=image,
            text=msg,
            buttons=buttons
        )
        await event.answer([results] if results else None)

@AnimeBot.on(events.InlineQuery(pattern='test ?(.*)'))
async def inline_test(event):
    query = event.pattern_match.group(1)
    variables = {'search': query}
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
    builder = event.builder
    r3 = builder.document(
        file=image,
        title="Hello World",
        description="Bruh",
        type="photo",
        text="Bruh",
        force_document=False)
    await AnimeBot(SetInlineBotResultsRequest(event.id,
        results=[r3],
        cache_time=0,
        gallery=False))