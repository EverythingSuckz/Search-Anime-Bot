from AnimeBot import AnimeBot
from telethon import events, Button
from ..helpers.search import shorten, anime_query, GRAPHQL
import requests
import telethon
from telethon.tl.types import BotInlineResult, InputBotInlineMessageMediaAuto, DocumentAttributeImageSize, InputWebDocument, InputBotInlineResult
from telethon.tl.functions.messages import SetInlineBotResultsRequest
from ..helpers.other import format_results

@AnimeBot.on(events.InlineQuery(pattern='anime ?(.*)'))
async def inline_anime(event):
    builder = event.builder
    query = event.pattern_match.group(1)
    variables = {'search': query}
    json = requests.post(GRAPHQL, json={'query': anime_query, 'variables': variables}).json()[
        'data'].get('Media', None)
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
        results = builder.photo(
            file=image,
            text=msg,
            buttons=buttons
        )
        await event.answer([results] if results else None)

##########CRAPS####################


@AnimeBot.on(events.InlineQuery(pattern='test ?(.*)'))
async def inline_test(event):
    query = event.pattern_match.group(1)
    variables = {'search': query}
    json = requests.post(GRAPHQL, json={'query': anime_query, 'variables': variables}).json()[
        'data'].get('Media', None)
    if json:
        msg, info, trailer, image = format_results(json)
    results=[InputBotInlineResult(
        id=event.id,
        type='photo',
        send_message=InputBotInlineMessageMediaAuto(msg),
        title=json['title']['romaji'],
        description='Nothin',
        url=info,
        thumb=InputWebDocument(
            url=image,
            size=42,
            mime_type='image/png',
            attributes=[DocumentAttributeImageSize(w=42, h=42)]
        ),
        content=InputWebDocument(
            url=image,
            size=42,
            mime_type='image/png',
            attributes=[DocumentAttributeImageSize(w=42, h=42)]
        )
    )]
    await AnimeBot(SetInlineBotResultsRequest(event.id,
        results=results,
        cache_time=0))

@AnimeBot.on(events.InlineQuery(pattern='something ?(.*)'))
async def inline_test2(event):
    query = event.pattern_match.group(1)
    variables = {'search': query}
    json = requests.post(GRAPHQL, json={'query': anime_query, 'variables': variables}).json()[
        'data'].get('Media', None)
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
    builder = event.builder
    size = DocumentAttributeImageSize(w=42, h=42)
    results = []
    results.append(builder.article(
        title=json['title']['romaji'],
        description=f"{json['format']} | {json.get('episodes', 'N/A')} Episodes",
        url=info,
        thumb=InputWebDocument(
            url=image,
            size=42,
            attributes=size,
            mime_type="image/png"
        ),
        content=InputWebDocument(
            url=image,
            size=42,
            attributes=size,
            mime_type="image/png"
        ),
        text=msg,
        buttons=buttons
    ))
    await event.answer(results if results else None)