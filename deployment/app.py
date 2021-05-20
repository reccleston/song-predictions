import os
from dotenv import load_dotenv

import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect
import pickle
from auxFunctions import *
from flask import Flask, jsonify, render_template, request



load_dotenv('.env')
POSTGRES_ID = os.getenv('POSTGRES_ID')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

engine = create_engine(f'{POSTGRES_ID}://{POSTGRES_PASSWORD}:postgres@localhost:5432/billboard_songs', echo=False)

Base = automap_base()
Base.prepare(engine, reflect=True)

connection = engine.connect()

model = pickle.load(open('models/LogRegW2021.sav','rb'))

app = Flask(__name__)

TopSongs = connection.execute("""SELECT * FROM songs;""")

# column_names = connection.execute("""SELECT *
#   FROM information_schema.columns
#  WHERE table_schema = 'public'
#    AND table_name   = 'songs'
#      ;""")

# @TODO:
# # SELECT ALL BUT SONG, ARTIST, ID, COLS FOR MATCHED SONGS TO BE PUT THROUGH
# # ADDING 0'S TO NEW DATA POINTS 
# # USING/ APPLIYING MODEL
# # PRETTIFY FRONT PIECE 

song_titles = []
song_list = []
data = []

for row in TopSongs:
    my_dict = {
        "song":row[0],
        "performer": row[1],
        "chart_position": row[2],
        "previous_position": row[3],
        "peak": row[4],
        "weeks_on_chart": row[5],
        "hitTF": row[6],
        "id": row[7],
        "danceability": row[8],
        "energy": row[9],
        "key": row[10],
        "loudness": row[11],
        "mode": row[12],
        "speechiness": row[13],
        "acousticness": row[14],
        "instrumentalness": row[15],
        "liveness": row[16],
        "valence": row[17],
        "tempo": row[18],
        "duratin_ms": row[19],
        "time_signature": row[20]
    }
    data.append(my_dict)
    song_titles.append(row[0])

data.append({'columns': ["song", "performer", "chart_position", "previous_position", "peak", "weeks_on_chart", "hitTF", "id", "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "duratin_ms", "time_signature"]})

@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/billboard_songs')
def songs():
    for song in TopSongs:
        song_titles.append(song[0])

    return jsonify(song_titles)

@app.route('/predict', methods=['POST'])
def predict():
    # test_features = get_features()

    pred = np.nan
    
    for users_input_song in request.form.values():
        if users_input_song in song_titles:
            print(users_input_song)
            # get other cols of data to for model 
            # song_info = connection.execute("""SELECT * EXCEPT song, performer, id FROM songs;""")
            song_info = getInfo(users_input_song, data)
            # for m in song_info:
            prediction = model.predict(song_info)
            print('LOOK HERE (from bb) -->', prediction)

            return render_template('index.html', prediction='ITS A HIT!')
        else:
            print(users_input_song)
            features = get_features(users_input_song)
            new_pt = makeNewPoint(features)
            prediction = model.predict(new_pt)

            print('LOOK HERE -->', prediction)

    
    # massage 

    # predict
    return render_template('index.html', prediction=pred)


# check if song is already in the top list 
# if not call spotify api to gather the songs audio features 
#     then massage this new data point into the shape needed to be run through the model 

if __name__ == "__main__":
    app.run(debug=True)