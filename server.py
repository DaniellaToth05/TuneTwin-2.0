# EDGE CASES: what if user doesn't enter any data

# import flask class so we can use it
# flask is a framework for building web apps, i.e. a toolbox for building websites
from flask import Flask, flash, redirect, render_template, request, url_for
from dotenv import load_dotenv
import lastfm
import spotify
import deezer
import os
import time

# creates an instance of the class flask, calls it app
app = Flask(__name__)

app.secret_key = 'b#K@d+f6Qw!ZpT4x2V9&0mNlXrS$yC3'

@app.route('/')
# create function that executes when user visits the url
def home_page():
    return render_template('index.html')

@app.route('/find-twin', methods=['POST'])
def find_twin():

    # get user inputted song and artist
    song = request.form.get('song')
    artist = request.form.get('artist')

    result = lastfm.find_song(song, artist)

    token = spotify.get_token()
    search_results = spotify.search_for_song(token, song, artist)

    tracks = []
    song_cover_url = ""
    song_name = song
    song_artist = artist

    if result:
        top_result = result[0]
        top_name = search_results.get("name", song_name) 
        top_artist = search_results.get("artists", [{}])[0].get("name", song_artist)  
        top_cover = search_results.get("album", {}).get("images", [{}])[0].get("url", "")

        twins = lastfm.find_match(top_name, top_artist) 
        tracks = twins[:10]

        for track in tracks:
            track_name = track.get("name")
            track_artist = track.get("artist", {}).get("name")
            deezer_artwork_url = deezer.get_artwork(track_name, track_artist)
            track["artwork"] = deezer_artwork_url

    return render_template(
        'find-twin.html',
        tracks=tracks,
        song_cover_url=top_cover,
        song_name=song,
        song_artist=artist
    )

if __name__ == '__main__':
    app.run(debug=True)

# get method: not secure data, typically typed in thru url or link
# post method: secure data, typically form data that won't be seen on either end or stored by the webserver unless we send it to a database

