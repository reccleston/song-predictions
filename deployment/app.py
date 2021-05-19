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

column_names = connection.execute("""SELECT *
  FROM information_schema.columns
 WHERE table_schema = 'public'
   AND table_name   = 'songs'
     ;""")

# @TODO:
# # SELECT ALL BUT SONG, ARTIST, ID, COLS FOR MATCHED SONGS TO BE PUT THROUGH
# # ADDING 0'S TO NEW DATA POINTS 
# # USING/ APPLIYING MODEL
# # PRETTIFY FRONT PIECE 

song_list = []


@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/billboard_songs')
def songs():
    for song in TopSongs:
        song_list.append(song[0])

    return jsonify(song_list)

@app.route('/predict', methods=['POST'])
def predict():
    # test_features = get_features()

    pred = np.nan

    for users_input_song in request.form.values():
        if users_input_song in song_list:
            # get other cols of data to for model 
            # song_info = connection.execute("""SELECT * EXCEPT song, performer, id FROM songs;""")
            song_info = getInfo(users_input_song, TopSongs)
            # for m in song_info:
            #     print(m)
            return render_template('index.html', prediction='ITS A HIT!')
        else:
            features = get_features(users_input_song)
            prediction_pt = makeTestPoint(features)

    
    # massage 

    # predict
    return render_template('index.html', prediction=pred)


# check if song is already in the top list 
# if not call spotify api to gather the songs audio features 
#     then massage this new data point into the shape needed to be run through the model 

if __name__ == "__main__":
    app.run(debug=True)