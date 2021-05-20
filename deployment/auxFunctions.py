import os
from dotenv import load_dotenv 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd 
import numpy as np
from sklearn.preprocessing import MinMaxScaler

load_dotenv('.env')
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))

def get_features(song):
    return spotify.audio_features(spotify.search(q=song, limit=1)['tracks']['items'][0]['uri'])[0]



# extract info from billboard list
def getInfo(song, SongList):
    for row in SongList:
        # print('inside for loop')
        for k in row.keys():
            if row[k] == song:
                return_entry = {k: row[k] for k in row if k not in ['song']}
                # print(row)
                # print(return_entry)
                return return_entry

def makeTestPoint(features):
    data = pd.DataFrame(features, [0]).select_dtypes(['int', 'float']).values
    print(data)
    scaler = MinMaxScaler().fit(data)
    X = scaler.transform(data)

    print('\n', X, '\n')
    # fill in the blank not on billboard hits 
    return 0

