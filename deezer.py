import requests

def get_artwork(song, artist):
    base_url = "https://api.deezer.com/search"
    query = f'track:"{song}" artist:"{artist}"'

    try:
        response = requests.get(base_url, params={"q": query}, timeout=5)

        if response.status_code == 200:
            data = response.json()
            if data.get("data"):
                track = data["data"][0]
                return track["album"]["cover_big"]

    except Exception as e:
        print(f"[Deezer Error] {e}")

    return None
