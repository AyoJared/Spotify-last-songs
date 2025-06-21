import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_spotify_tracks(limit=30):
    url = "https://api.spotify.com/v1/playlists/6UeSakyzhiEt4NB3UAd6NQ/tracks"
    headers = {
        "Authorization": f"Bearer {os.getenv('API_KEY')}",
        "Content-Type": "application/json"
    }
    params = {"limit": limit}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        tracks = []
        for item in data['items']:
            track = item['track']
            if not track:  # skip broken entries
                continue
            name = track['name']
            artists = ", ".join(artist['name'] for artist in track['artists'])
            album_images = track['album']['images']
            image_url = album_images[0]['url'] if album_images else None

            tracks.append({
                "id": track['id'],
                "name": name,
                "artist": artists,
                "image_url": image_url
            })
        return tracks
    else:
        print(f"❌ Failed to fetch data from Spotify (status code: {response.status_code})")
        return []
