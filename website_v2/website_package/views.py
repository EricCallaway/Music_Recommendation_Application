from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from flask_mysqldb import MySQL
from sqlalchemy import text, create_engine
from .models import Note, User, Pet, Billboard
from decimal import Decimal
from . import db 
from scipy.spatial.distance import cosine
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List

import numpy as np
import pandas as pd
import json
import joblib
import MySQLdb.cursors

#Creating blueprint named "views"
views = Blueprint('views', __name__)

def generate_recommendations(user_playlist_song_ids: List[str]) -> list[str]:
    """
    Generates song recommendations based on the user's playlist.
    
    Parameters - user_playlist_song_ids: list of strings represented as spotify ids of songs in the user's playlist

    Returns - recommended_songs: list of strings represented as spotify ids of songs recommended to the user
    """

    # Connect to the database
    engine = create_engine('mysql://root:Eric19$$@localhost:3306/music_app')
    connection = engine.connect()

    # Query the database for all the data in the billboard table
    query = text('SELECT * FROM billboard;')

    # Fetch all the data from the database using the query defined above
    all_data = connection.execute(query).fetchall()

    # Close the connection to the database
    connection.close()

    # Convert the all data to a pandas dataframe
    all_data = pd.DataFrame(all_data)

    # Rename columns of all_data
    all_data.rename(columns={0: 'date',
                             1: 'title',
                             2: 'artist',
                             3: 'spotify_link',
                             4: 'spotify_id',
                             21: 'clean_lyrics'}, inplace=True)
    
    # Drop the columns that are not needed and assign to new dataframe
    data = all_data[['title', 'artist', 'spotify_id', 'clean_lyrics']]

    # Create a Tf-Idf Vectorizer Object
    vectorizer = TfidfVectorizer()

    # Fit the vectorizer to the clean lyrics, creating a tf-idf matrix where the words are the features
    tfidf_matrix = vectorizer.fit_transform(all_data['clean_lyrics'])

    # Transform the user playlist into a tf-idf matrix
    user_playlist_lyrics = data[data['spotify_id'].isin(user_playlist_song_ids)]['clean_lyrics'].tolist()
    user_playlist_tfidf = vectorizer.transform(user_playlist_lyrics)

    # Calculate the cosine similarity between the user playlist and the billboard songs
    cosine_similarities = cosine_similarity(user_playlist_tfidf, tfidf_matrix).flatten()

    # Reduce the number of indices to 6775, the number of indices was upwards of 20,000 for some reason
    cosine_similarities = cosine_similarities[:6775]

    # Sort the indices by similarity score in descending order
    song_indices = cosine_similarities.argsort()[::-1]

    # Create a list of recommended songs
    recommended_songs = []
    for i in song_indices:
        if data.loc[i, 'spotify_id'] in user_playlist_song_ids:
            continue
        else:
            recommended_songs.append(data.loc[i, 'spotify_id'])
            if len(recommended_songs) == 5:
                break

    return recommended_songs


@views.route('/tf_idf', methods=['GET', 'POST'])
@login_required
def tf_idf():
    # Get the user's playlist
    recommended_songs = []

    # When the user submits the form 
    if request.method == 'POST':
        playlist = []
        for i in range(len(request.form)):
            song = request.form.get(f'song{i}')
            if song:
                playlist.append(song)
         
         # Generate recommendations
        recommended_songs = generate_recommendations(playlist)

        # Query the database for the recommended songs
        recommended_song_ids = [f"'{song}'" for song in recommended_songs]
        sql_recommended_songs = text(f'SELECT title, artist, spotify_link, spotify_id FROM billboard WHERE spotify_id IN ({", ".join(recommended_song_ids)});')
        session = db.session()
        try:
            cursor = session.execute(sql_recommended_songs).cursor
            recommended_songs = cursor.fetchall()
        except Exception as e:
            print("Error executing query: ", e)
            session.rollback()
        finally:
            session.close()

    return render_template('tf_idf.html', user=current_user, recommended_songs=recommended_songs)

@views.route('api/billboard_songs')
def billboard_song_data():
    query = Billboard.query

    #search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            Billboard.name.like(f'%{search}%'),
            Billboard.artist.like(f'%{search}%')
        ))
    total_filtered = query.count()

    #sorting
    order = []
    cols = [
        'date', 'title', 'artist', 'spotify_link', 'spotify_id',
        'genre', 'analysis_url', 'energy', 'liveness', 'tempo', 'speechiness',
        'acousticness', 'instrmentalness', 'time_signature', 'danceability', 
        'key', 'duration_ms', 'loudness', 'valence', 'mode', 'lyrics', 'clean_lyrics'
    ]
    i = 0 
    
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in cols:
            col_name = 'title'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(Billboard, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1

    if order:
        query = query.order_by(*order)

    #pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    #response
    return {
        'data': [billboard.to_dict() for billboard in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': Billboard.query.count(),
        'draw': request.args.get('draw', type=int),
    }



@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
   
    return render_template("home.html", user=current_user)

@views.route('/songs', methods=['GET', 'POST'])
def display_songs():
    songs = Billboard.query
    return render_template('songs.html', songs=songs, user=current_user)

#This method will allow the user to add new songs
@views.route('/new_song', methods=['GET', 'POST'])
def add_song():
    if request.method == 'POST':
        name = request.form.get('name')
        artist = request.form.get('artist')
        new_song = Song(name=name, artist=artist)
        db.session.add(new_song)
        db.session.commit()
        return redirect(url_for('views.display_songs'))
    return render_template('new_song.html', user=current_user)

#This endpoint will return a JSON payload required for the Ajax Data Source
@views.route('api/data')
def song_data():
    query = Song.query

    #search filter
    search = request.args.get('search[value]')
    if search:
        query = query.filter(db.or_(
            Song.name.like(f'%{search}%'),
            Song.artist.like(f'%{search}%')
        ))

    total_filtered = query.count()

    #sorting
    order = []
    cols = [
        'track_id', 'track_name', 'track_artist', 'lyrics', 'track_album_id' , 'playlist_name',
        'playlist_id', 'playlist_genre', 'playlist_subgenre', 'danceability', 'energy' , 'key',
        'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'language']
    i = 0
    while True:
        col_index = request.args.get(f'order[{i}][column]')
        if col_index is None:
            break
        col_name = request.args.get(f'columns[{col_index}][data]')
        if col_name not in cols:
            col_name = 'track_name'
        descending = request.args.get(f'order[{i}][dir]') == 'desc'
        col = getattr(Song, col_name)
        if descending:
            col = col.desc()
        order.append(col)
        i += 1
    
    if order:
        query = query.order_by(*order)

    #pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    #response
    return {
        'data': [song.to_dict() for song in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': Song.query.count(),
        'draw': request.args.get('draw', type=int),
    }


@views.route('/pets', methods = ['GET', 'POST'])
def show_pet():
    pets = Pet.query.all()
    return render_template('pets.html', user=current_user, pets=pets)

@views.route('/fruits', methods=['GET', 'POST'])
def fruits():
    if request.method == 'POST':
        fruit = []
        fruit.append(request.form.get('fruit_input'))
        print(fruit)
    return render_template('fruits.html', user=current_user)