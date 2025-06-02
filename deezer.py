import requests

def get_song_details(song, artist):
    base_url = "https://api.deezer.com/search"
    query = f'track:"{song}" artist:"{artist}"'
    
    response = requests.get(base_url, params={"q": query})

    if response.status_code == 200:
        data = response.json()
        if data["data"]:  # if any results
            track_info = data["data"][0]
            return {
                "cover": track_info["album"]["cover_big"],
                "preview": track_info["preview"]
            }
    
    # Fallbacks
    return {
        "cover": "static/images/default.jpg",
        "preview": None
    }
