import os
from dotenv import load_dotenv 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv('.env')
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))

# def get_song_uri(song, artist=None): 
#     return spotify.search(q=song, limit=1)['tracks']['items'][0]['uri']

def get_features(song):
    return spotify.audio_features(spotify.search(q=song, limit=1)['tracks']['items'][0]['uri'])[0]