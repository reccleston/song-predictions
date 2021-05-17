import os
from dotenv import load_dotenv

import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect
import pickle

from flask import Flask, jsonify, render_template

load_dotenv('.env')
POSTGRES_ID = os.getenv('POSTGRES_ID')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

engine = create_engine(f'{POSTGRES_ID}://{POSTGRES_PASSWORD}:postgres@localhost:5432/billboard_songs', echo=False)

Base = automap_base()
Base.prepare(engine, reflect=True)

connection = engine.connect()

model = pickle.load(open('models/LogRegW2021.sav','rb'))

app = Flask(__name__)

@app.route('/')
def home():
    TopSongs = connection.execute("""SELECT * FROM songs;""")
    data = []
    for song in TopSongs:
        data.append({'song': song[0],
                     'performer': song[1],
                     'chart_position': song[2],
                     'previous_postion': song[3],
                     'peak': song[4],
                     'weeks_on_chart': song[5],
                     'danceability': song[8],
                     'engery': song[9],
                     'key': song[10],
                     'loudness': song[11],
                     'mode': song[12],
                     'speechiness': song[13],
                     'acousticness': song[14],
                     'instrumentalness': song[15],
                     'liveness': song[16],
                     'valence': song[17],
                     'tempo': song[18],
                     'duration_ms': song[19],
                     'time_signature': song[20]})

    # Dates = connection.execute("""SELECT * FROM dates;""")
    # dont forgoet to start/end session
    return jsonify(data)

# check if song is already in the top list 
# if not call spotify api to gather the songs audio features 
#     then massage this new data point into the shape needed to be run through the model 

if __name__ == "__main__":
    app.run(debug=True)