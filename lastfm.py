from dotenv import load_dotenv
import os
import base64
import json
import requests

load_dotenv()

api_key = os.getenv("API_KEY")
lastfm_url = "https://ws.audioscrobbler.com/2.0/"

def find_song(song, artist):

    params = {
        "method": "track.search",
        "track": song,
        "artist": artist,
        "api_key": api_key,
        "format": "json",
    }

    response = requests.get(lastfm_url, params=params)

    if response.status_code == 200:
        return response.json().get("results", {}).get("trackmatches", {}).get("track", [])

    return []

def find_match(song, artist):

    params = {
        "method": "track.getsimilar",
        "track": song,
        "artist": artist,
        "api_key": api_key,
        "format": "json",
    }
    response = requests.get(lastfm_url, params=params)

    if response.status_code == 200:
        return response.json().get("similartracks", {}).get("track", [])

    return []
