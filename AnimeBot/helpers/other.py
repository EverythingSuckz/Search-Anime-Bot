import requests
from .search import shorten


def conv_to_jpeg(image):
    response = requests.get(image)
    file_name = "anilist.jpg"
    file = open(file_name, "wb")
    file.write(response.content)
    file.close()
    return file_name


def format_results(json):
    msg = f"""
**{json['title']['romaji']}**(`{json['title']['native']}`)
**Type**: {json['format']}
**Status**: {json['status']}
**Episodes**: {json.get('episodes', 'N/A')}
**Duration**: {json.get('duration', 'N/A')} Per Ep.
**Score**: {json['averageScore']}
**Genres**: `
"""
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
    description = json.get('description', 'N/A').replace('<i>', '').replace('</i>', '').replace('<br>', '')
    msg += shorten(description, info)
    image = info.replace('anilist.co/anime/', 'img.anili.st/media/')
    return msg, info, trailer, image