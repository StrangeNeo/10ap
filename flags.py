import sys
from PIL import Image
import requests
from io import BytesIO


here = sys.argv[1:]


def apt(coords):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    coords = ','.join(coords)
    search_params = {
        "apikey": api_key,
        "text": "аптека",
        "lang": "ru_RU",
        "ll": coords,
        'results': '10'
    }
    response = requests.get(search_api_server, params=search_params)
    if not response:
        sys.exit(0)
    else:
        pt = ''
        for i in range(10):
            apteka = response.json()['features'][i]
            coordinat = f"{apteka['geometry']['coordinates'][0]},{apteka['geometry']['coordinates'][1]}"
            try:
                hour24 = apteka['properties']['CompanyMetaData']['Hours']['Availabilities'][0]['TwentyFourHours']
            except Exception as e:
                hour24 = 'Нэту'
            if hour24 == 'Нэту':
                pt += f'{coordinat},pm2grl~'
            elif hour24 == True:
                pt += f'{coordinat},pm2dgl~'
            else:
                pt += f'{coordinat},pm2bll~'
        pt = pt[:-1]
        return pt


map_params = {
    "l": "map",
    "pt": apt(here)
}
map_api_server = "http://static-maps.yandex.ru/1.x/"

response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(response.content)).show()

