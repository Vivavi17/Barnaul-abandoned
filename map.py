import os.path

import requests
import json
from bs4 import BeautifulSoup
import googlemaps
import folium


def get_addresses():
    resp = requests.get('https://dom.mingkh.ru/avarijnye/altayskiy-kray/barnaul/')
    html = resp.text
    soup = BeautifulSoup(html, 'html.parser')
    addresses = [i.text for i in soup.find_all('a', href=True) if 'ул. ' in i.text]
    return addresses


def read_key():
    with open('key.txt', 'r') as f:
        key = f.read()
    return key


def get_coordinates(addresses):
    gmaps = googlemaps.Client(key=read_key())
    # geocode= gmaps.geocode('Барнаул'+addresses[0])
    # print(geocode[0]['geometry']['location'])
    geocode = [
        {
            'adr': adr,
            'geocode': gmaps.geocode('Барнаул' + adr)
        }
        for adr in addresses if gmaps.geocode('Барнаул' + adr)
    ]
    print(geocode[0])
    coordinates = [{'adr': element['adr'], **element['geocode'][0]['geometry']['location']}
                   for element in geocode]
    print()
    # coordinates = [{geocode[i]: geocode[i][geocode[i]][0]['geometry']['location']} for i in range(len(geocode))]
    print(coordinates[0])
    return coordinates


def save_adr(adr, coords):
    with open('addresses.json', 'w') as f:
        json.dump(adr, f)

    with open('coordinates.json', 'w') as f:
        json.dump(coords, f)


def load():
    if os.path.exists('coordinates.json'):
        with open('coordinates.json', 'r') as file2:
            coord = json.load(file2)
    else:
        adresses = get_addresses()
        coords = get_coordinates(adresses)
        save_adr(adresses, coords)
    return coord


def map_markers(coordinates):
    # m = folium.Map(location=(53.3678038, 83.759705))
    m = folium.Map([53.3678038, 83.759705], zoom_start=12)
    for val in coordinates:
        folium.Marker(
            location=[val['lat'], val['lng']],
            tooltip="заброшка",
            popup=val['adr'],
            icon=folium.Icon(color="red"),
        ).add_to(m)
    m.save("zabroshki.html")


if __name__ == '__main__':
    coordinates = load()
    map_markers(coordinates)
