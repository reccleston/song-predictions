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


# postgres credentials
load_dotenv('.env')
POSTGRES_ID = os.getenv('POSTGRES_ID')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

# connect to DB
# connection string
engine = create_engine(f'{POSTGRES_ID}://{POSTGRES_PASSWORD}:postgres@localhost:5432/billboard_songs', echo=False)

Base = automap_base()
Base.prepare(engine, reflect=True)
# connect to DB
connection = engine.connect()

# load model
model = pickle.load(open('models/LogRegW2021.sav','rb'))

app = Flask(__name__)

# query for all songs info
TopSongs = connection.execute("""SELECT * FROM songs;""")

# lists to hold song info from DB
song_titles = []
song_list = []
data = []

# iterating over return from DB and appending to dict
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

# home route
@app.route('/')
def home():
    return render_template('index.html')

# song append route (is this necess?)
@app.route('/billboard_songs')
def songs():
    for song in TopSongs:
        song_titles.append(song[0])

    return jsonify(song_titles)

# prediction route
@app.route('/predict', methods=['POST'])
def predict():
    # test_features = get_features()

    # pred = np.nan
    predictText = ''
    # compare user input to song titles
    for users_input_song in request.form.values():
        # if the input is in the titles
        if users_input_song in song_titles:
            print(users_input_song)
            # send to getInfo funct to get the data
            song_info = getInfo(users_input_song, data)
            # run the song info through the model
            prediction = model.predict(song_info)
            print('LOOK HERE (from bb) -->', prediction)
            # if the prediction is 'not a hit', send 'no hit' message
            if prediction == 0:
                predictText = f'{users_input_song} is likely to not be a hit!'
                return render_template('index.html', text = predictText)
            # if prediction is 'hit', send 'hit' message
            elif prediction == 1:
                predictText = f'{users_input_song} is likely to be a hit!'
                return render_template('index.html', text = predictText)
        # if song is not in titles
        else:
            print(users_input_song)
            # send to get_features funct with Spotify API
            features = get_features(users_input_song)
            # send to makeNewPoint funct to append zeros
            new_pt = makeNewPoint(features)
            # run the song through the model
            prediction = model.predict(new_pt)
            # if the prediction is 'not a hit', send 'no hit' message
            if prediction == 0:
                predictText = f'{users_input_song} is likely to not be a hit!'
                return render_template('index.html', text = predictText)
            # if prediction is 'hit', send 'hit' message
            elif prediction == 1:
                predictText = f'{users_input_song} is likely to be a hit!'
                return render_template('index.html', text = predictText)


if __name__ == "__main__":
    app.run(debug=True)