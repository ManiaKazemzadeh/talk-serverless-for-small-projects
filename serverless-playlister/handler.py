import json
from ytmusicapi import YTMusic
import requests
from bs4 import BeautifulSoup
import logging


def create_playlist(logger):
    ytmusic = YTMusic('headers_auth.json')

    # Create playlist
    ytmusicPlaylistID = ytmusic.create_playlist(
        "BBC 6 Music Playlist", "The BBC 6 Music playlist")

    logger.info("Playlist created")

    # Fetch bbc music playlist and put the song names in a list
    request = requests.get(
        'https://www.bbc.co.uk/programmes/articles/5JDPyPdDGs3yCLdtPhGgWM7/bbc-radio-6-music-playlist')
    soup = BeautifulSoup(request.text, 'html.parser')

    logger.info("Fetched song names")

    all_p = soup.find_all('p')
    filtered_p = []
    for p in all_p:
        if " - " in p.get_text():
            filtered_p.append(p.get_text())

    # Search for songs
    songs = []

    for song in filtered_p:
        result = ytmusic.search(song, "songs")[0]
        if result["title"] in song and result["artists"][0]["name"] in song:
            songs.append(result["videoId"])

    logger.info("Adding songs to youtube")

    # Add songs to youtube music playlist
    ytmusic.add_playlist_items(ytmusicPlaylistID, songs)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def run(event, context):
    create_playlist(logger)

    body = {
        "message": "Go Serverless v3.0! Your function executed successfully!",
        "input": event,
    }

    response = {"statusCode": 200, "body": json.dumps(body)}

    return response
