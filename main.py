import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

user_choice_date = input("Which day do you want to travel to? Type the date in this format YYYY-MM-DD: ")

URL = f"https://www.billboard.com/charts/hot-100/{user_choice_date}"

response = requests.get(URL)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')
songs = soup.find_all(name='span', class_='chart-element__information__song text--truncate color--primary')
song_names = []
for song in songs:
    song_names.append(song.getText())

client_id = os.environ.get("id")
client_secret = os.environ.get("secret")
redirect_url = os.environ.get("url")

auth_manager = SpotifyOAuth(client_id=client_id, client_secret=client_secret,
                            scope='playlist-modify-private playlist-modify-public',
                            redirect_uri=redirect_url, show_dialog=True, cache_path='Token.txt')
spotify = spotipy.Spotify(auth_manager=auth_manager)

user_id = os.environ.get("user_id")

search_results = []
for name in song_names:
    search = spotify.search(q=f"track: {name} year:{user_choice_date[:4]}", type='track', limit=50)
    try:
        uri = search['tracks']['items'][0]['uri']
    except IndexError:
        pass
    else:
        search_results.append(uri)


playlist = spotify.user_playlist_create(user=user_id, name=f"{user_choice_date} Billboard 100",
                                        public=True)

spotify.playlist_add_items(playlist_id=playlist['id'], items=search_results)
