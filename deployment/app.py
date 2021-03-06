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
model = pickle.load(open('models/LogReg.sav','rb'))

app = Flask(__name__)

# query for all billboard songs info
TopSongs = connection.execute("""SELECT * FROM songs;""")

# lists to hold song info from billboard DB
song_titles = []
bbData = []
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
    bbData.append(my_dict)
    song_titles.append(row[0])

bbData.append({'columns': ["song", "performer", "chart_position", "previous_position", "peak", "weeks_on_chart", "hitTF", "id", "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "duratin_ms", "time_signature"]})

# the algorithm route
@app.route('/')
def home():
    return render_template('index.html')

# the tracks page
@app.route('/tracks')
def tracks():
    return render_template("tracks.html")

# route to display the sunburst chart
@app.route('/sunburstbubble')
def sunbubblevalues():
    result = connection.execute("""SELECT * FROM data_cleaned;""")
    # print(result)
    data = []
    for row in result:
        my_dict = {
            "title":row[0],
            "artist": row[1],
            "genre": row[2],
            "genre_num": row[3],
            "subgenre": row[4],
            "year": row[5],
            "bpm": row[6],
            "nrgy": row[7],
            "dnce": row[8],
            "dB": row[9],
            "live": row[10],
            "val": row[11],
            "dur": row[12],
            "acous": row[13],
            "spch": row[14],
            "pop": row[15]
        }
        data.append(my_dict)
        # print(row)
    data.append({'columns': ["title", "artist", "genre", "genre_num", "subgenre", "year", "bpm", "nrgy", "dnce", "dB", "live", "val", "dur", "acous", "spch", "pop"]})
    return(jsonify(data))

# route to display heatmap
@app.route('/heatmap')
def heatmapvalues():
    result = connection.execute("""SELECT * FROM corr_heatmap_vals;""")
    data = []
    for row in result:
        my_dict = {
            "feat1":row[0],
            "feat2": row[1],
            "vals": row[2]
        }
        data.append(my_dict)
        # print(row)
    return(jsonify(data))

# route to display bar graph
@app.route('/bar')
def barvalues():
    result = connection.execute("""SELECT * FROM year_table;""")
    data = []
    for row in result:
        my_dict = {
            "year":row[0],
            "nrgy": row[1],
            "dnce": row[2],
            "val": row[3],
            "pop": row[4]
        }
        data.append(my_dict)
        # print(row)
    return(jsonify(data))

# route to create a songs list - might not be necessary 
@app.route('/billboard_songs')
def songs():
    for song in TopSongs:
        song_titles.append(song[0])

    return jsonify(song_titles)

# route to obtain and display predictions
@app.route('/predict', methods=['POST'])
def predict():
    
    predictText = ''
    for users_input_song in request.form.values():
        if users_input_song in song_titles:
            # print(users_input_song)
            song_info = getInfo(users_input_song, bbData)
            # for m in song_info:
            print('here-->', song_info)
            prediction = model.predict(song_info)
            # print('LOOK HERE (from bb) -->', prediction)
            if prediction == 0:
                predictText = f'{users_input_song} is likely to not be a hit!'
                return render_template('index.html', text = predictText)
            elif prediction == 1:
                predictText = f'{users_input_song} is likely to be a hit!'
                return render_template('index.html', text = predictText)            

        else:
            # print(users_input_song)
            features = get_features(users_input_song)
            new_pt = makeNewPoint(features)

            print('there==>', new_pt)
            prediction = model.predict(new_pt)
            drake = [[5.60000000e-01, 0.00000000e+00, 5.60000000e-01, 2.17391304e-02,
        7.13993871e-01, 6.86993802e-01, 6.36363636e-01, 9.17823175e-01,
        0.00000000e+00, 1.10994764e-01, 3.09236948e-01, 3.66666667e-05,
        1.22469636e-01, 5.10747185e-01, 4.19553895e-01, 4.59569349e-02,
        8.00000000e-01]]
            print(drake)
            print('pred for drake song', model.predict(drake))
            # print('LOOK HERE -->', prediction)

            if prediction == 0:
                predictText = f'{users_input_song} is likely to not be a hit!'
                return render_template('index.html', text = predictText)
            elif prediction == 1:
                predictText = f'{users_input_song} is likely to be a hit!'
                return render_template('index.html', text = predictText)

if __name__ == "__main__":
    app.run(debug=True, port=5000)