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
    return render_template('index.html')
    
@app.route('/billboard_songs')
def songs():
    TopSongs = connection.execute("""SELECT * FROM songs;""")
    song_titles = []
    for song in TopSongs:
        song_titles.append(song[0])

    # Dates = connection.execute("""SELECT * FROM dates;""")
    # dont forgoet to start/end session
    return jsonify(song_titles)

# check if song is already in the top list 
# if not call spotify api to gather the songs audio features 
#     then massage this new data point into the shape needed to be run through the model 

if __name__ == "__main__":
    app.run(debug=True)