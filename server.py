# EDGE CASES: what if user doesn't enter any data

# import flask class so we can use it
# flask is a framework for building web apps, i.e. a toolbox for building websites
# server.py
from flask import Flask, render_template, request, jsonify
import random
from deezer import get_song_details  # Import the updated function
from lastfm import find_match

app = Flask(__name__)

# Song list (same as before)
SONGS = [
    {
        "title": "Nights",
        "artist": "Frank Ocean",
        "description": "a two-part odyssey through heartbreak and reinvention. the glow-up anthem for lonely nights.",
        "quote": "\"every night fucks every day up<br>every day patches the night up\"",
        "tags": ["moody", "layered", "late night", "transcendent"],
    },
    {
        "title": "Objects in the Mirror",
        "artist": "Mac Miller",
        "description": "gentle reflection and soulful honesty — the warmth of late night self-awareness.",
        "quote": "\"people love you when they on your mind<br>a thought is love’s currency\"",
        "tags": ["jazzy", "self-aware", "smooth", "melancholy"],
    },
    {
        "title": "Ribs",
        "artist": "Lorde",
        "description": "nostalgia wrapped in echo — the terrifying sweetness of growing older too fast.",
        "quote": "\"it feels so scary getting old\"",
        "tags": ["nostalgic", "youth", "aching", "echoey"],
    },
    {
        "title": "Roslyn",
        "artist": "Bon Iver & St. Vincent",
        "description": "haunting harmonies echoing the ache of isolation and delicate memories.",
        "quote": "\"up with your head down<br>and your eyes closed\"",
        "tags": ["ethereal", "soft", "aching", "winter"],
    },
    {
        "title": "Motion Picture Soundtrack",
        "artist": "Radiohead",
        "description": "a funeral lullaby for broken hearts and faded futures.",
        "quote": "\"i will see you in the next life\"",
        "tags": ["cinematic", "haunting", "slow", "dramatic"],
    },
    {
        "title": "Lost",
        "artist": "Frank Ocean",
        "description": "caught between freedom and chaos — a sun-drenched loop of longing.",
        "quote": "\"double D, big full breasts on my baby\"",
        "tags": ["groovy", "bittersweet", "playful", "addictive"],
    },
    {
        "title": "Cherry Wine",
        "artist": "Hozier",
        "description": "gentle guitar, raw confessions — the softness of complicated love.",
        "quote": "\"the way she tells me I’m hers and she is mine\"",
        "tags": ["tender", "raw", "folk", "intimate"],
    },
]

def build_song_data(raw_song):
    """Attach Deezer artwork and preview to a song dictionary."""
    details = get_song_details(raw_song["title"], raw_song["artist"])
    return {
        **raw_song,
        "album_cover": details["cover"],
        "preview_url": details["preview"]
    }

@app.route('/', methods=['GET'])
def home():
    selected = random.choice(SONGS)
    song = build_song_data(selected)
    return render_template('index.html', song=song)

@app.route('/refresh', methods=['POST'])
def refresh():
    selected = random.choice(SONGS)
    song = build_song_data(selected)
    return render_template('partials/tonight_song.html', song=song)

@app.route('/search', methods=['GET'])
def search_page():
    return render_template('search.html')

@app.route('/search-song', methods=['POST'])
def search_song():
    data = request.json
    song = data.get('song')
    artist = data.get('artist')

    if not song or not artist:
        return jsonify({'error': 'Song and artist are required.'}), 400

    matches = find_match(song, artist)

    result_data = []
    for match in matches[:2]:  # Limit to top 2 matches
        title = match.get('name')
        artist_name = match.get('artist', {}).get('name')
        description = "A match based on emotional tone and mood."
        tags = ['emotional', 'introspective', 'melodic', 'moody']
        details = get_song_details(title, artist_name)
        cover = details['cover']

        result_data.append({
            'title': title,
            'artist': artist_name,
            'description': description,
            'tags': tags,
            'album_cover': cover
        })

    return jsonify(result_data)

if __name__ == '__main__':
    app.run(debug=True)

# get method: not secure data, typically typed in thru url or link
# post method: secure data, typically form data that won't be seen on either end or stored by the webserver unless we send it to a database