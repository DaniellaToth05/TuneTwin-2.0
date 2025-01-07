# EDGE CASES: what if user doesn't enter any data

# Import flask class so we can use it
# Flask is a framework for building web apps, i.e. a toolbox for building websites
from flask import Flask, flash, redirect, render_template, request, url_for
from dotenv import load_dotenv
import lastfm
import os

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

    tracks = []
    song_cover_url = ""
    song_name = song
    song_artist = artist

    if result:
        top_result = result[0]
        top_name = top_result.get("name", song_name)
        top_artist = top_result.get("artist", song_artist)
        top_cover = top_result.get("image", [{}])[-1].get("#text", "")  # largest image url at -1 (others are for thumbnails)   

        twins = lastfm.find_match(top_name, top_artist) 
        tracks = twins[:10]

    return render_template(
        'find-twin.html',
        tracks=tracks,
        song_cover_url=top_cover,
        song_name=song,
        song_artist=artist
    )


    # token = spotify.get_token()
    # search_results = spotify.search_for_song(token, song, artist)

    # tracks = []
    # song_cover_url = ""
    # song_name = song
    # song_artist = artist

    # if search_results:
    #     track_id = search_results.get("id")
    #     song_cover_url = search_results.get("album", {}).get("images", [{}])[0].get("url", "")
    #     song_name = search_results.get("name", song_name)  # Use the song name from search results if available
    #     song_artist = search_results.get("artists", [{}])[0].get("name", song_artist)  # Use the artist name from search results if available
    #     recommendations = spotify.get_recs(token, seed_tracks=track_id)

    #     if recommendations:
    #         tracks = recommendations.get('tracks', [])  # This should now only contain 10 tracks


    # return render_template('find-twin.html', tracks=tracks, song_cover_url=song_cover_url, song_name=song_name, song_artist=song_artist)




# @app.route("/<word>")
# def user(word):
#     return f"Where do you think you're going? {word} doesn't exist!"

# @app.route("/secret/")
# def secret():
#     return redirect(url_for("user", word="Secret"))

if __name__ == '__main__':
    app.run(debug=True)

# get method: not secure data, typically typed in thru url or link
# post method: secure data, typically form data that won't be seen on either end or stored by the webserver unless we send it to a database



# from flask import Flask, request, render_template, jsonify
# import requests

# app = Flask(__name__)

# LASTFM_API_KEY = "9d6466a9f6409f63680eb9c885419ba3"
# LASTFM_BASE_URL = "https://ws.audioscrobbler.com/2.0/"

# def search_track(song, artist):
#     """Search for a song and artist on Last.fm."""
#     params = {
#         "method": "track.search",
#         "track": song,
#         "artist": artist,
#         "api_key": LASTFM_API_KEY,
#         "format": "json",
#     }
#     response = requests.get(LASTFM_BASE_URL, params=params)
#     if response.status_code == 200:
#         return response.json().get("results", {}).get("trackmatches", {}).get("track", [])
#     return []

# def get_similar_tracks(song, artist):
#     """Get similar tracks from Last.fm."""
#     params = {
#         "method": "track.getsimilar",
#         "track": song,
#         "artist": artist,
#         "api_key": LASTFM_API_KEY,
#         "format": "json",
#     }
#     response = requests.get(LASTFM_BASE_URL, params=params)
#     if response.status_code == 200:
#         return response.json().get("similartracks", {}).get("track", [])
#     return []

# @app.route('/find-twin', methods=['POST'])
# def find_twin():
#     song = request.form.get('song')
#     artist = request.form.get('artist')

#     # Search for the song and artist
#     search_results = search_track(song, artist)

#     # Default values
#     tracks = []
#     song_cover_url = ""
#     song_name = song
#     song_artist = artist

#     if search_results:
#         # Use the first search result for more accurate recommendations
#         first_result = search_results[0]
#         song_name = first_result.get("name", song_name)
#         song_artist = first_result.get("artist", song_artist)
#         song_cover_url = first_result.get("image", [{}])[-1].get("#text", "")  # Get the largest image URL

#         # Get similar tracks
#         recommendations = get_similar_tracks(song_name, song_artist)
#         tracks = recommendations[:10]  # Limit to 10 recommendations

#     return render_template(
#         'find-twin.html',
#         tracks=tracks,
#         song_cover_url=song_cover_url,
#         song_name=song_name,
#         song_artist=song_artist
#     )

# if __name__ == '__main__':
#     app.run(debug=True)
