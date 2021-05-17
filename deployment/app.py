import os
from dotenv import load_dotenv

import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect
import pickle
from get_audio_features import get_features
from massageData import getInfo
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
song_titles = []

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

    for song_title in request.form.values():
        if song_title in song_titles:
            song_info = getInfo(song_title, TopSongs)
            return render_template('index.html', prediction='ITS A HIT!')
        else:
            pred = get_features(song_title)
    
    # massage 

    # predict
    return render_template('index.html', prediction=pred)


# check if song is already in the top list 
# if not call spotify api to gather the songs audio features 
#     then massage this new data point into the shape needed to be run through the model 

if __name__ == "__main__":
    app.run(debug=True)