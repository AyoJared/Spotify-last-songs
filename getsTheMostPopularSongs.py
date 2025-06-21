import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Billboard Hot 100
url = "https://api.spotify.com/v1/playlists/6UeSakyzhiEt4NB3UAd6NQ/tracks"

headers = {
    "Authorization": f"Bearer {os.getenv('API_KEY')}",
    "Content-Type": "application/json"
}
params = {
    # Max Limit is 100
    "limit": 30
}


response = requests.get(url, headers=headers, params= params)


if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    count = 1
    for item in data['items']:
        track = item['track']
        song = track['name']
        artists = ", ".join(artist['name'] for artist in track['artists'])
        print(f"{count}: {song} - {artists}")
        count+=1
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")