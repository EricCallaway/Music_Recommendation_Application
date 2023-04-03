from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from flask_mysqldb import MySQL
from sqlalchemy import text
from .models import Note, Song, User, Pet, Billboard
from decimal import Decimal
from . import db 
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import cosine

import numpy as np
import json
import joblib
import MySQLdb.cursors

#Creating blueprint named "views"
views = Blueprint('views', __name__)

def pad_and_reshape(arr):
    num_rows, num_cols = arr.shape[1], arr.shape[2]
    col_avgs = np.mean(arr, axis=1).reshape(-1, num_cols) # calculate the average of each column
    padded_arr = np.empty((1, 35, 12))
    padded_arr.fill(np.nan) # fill with NaN values initially

    # copy original array to padded array
    padded_arr[:, :num_rows, :num_cols] = arr

    # pad remaining rows with average of each column
    for i in range(num_rows, 35):
        padded_arr[:, i] = col_avgs

    return padded_arr

@views.route('/tf_idf', methods=['GET', 'POST'])
@login_required
def tf_idf():
    return render_template('tf_idf.html', user=current_user)

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
        'id', 'date', 'title', 'artist', 'spotify_link', 'spotify_id',
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
    recommended_track_ids = []
    recommended_tracks = ""
    if request.method == 'POST':
        audio_cols = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms']
        playlist = []
        input_seq = []
        master_audio_feats = []
        for i in range(len(request.form)):
            song = request.form.get(f'song{i}')
            if song:
                playlist.append(song)
        print('$'*50)
        print(playlist)
        print('$'*50)
        print(len(request.form))
        

        model = joblib.load('training_model/simpleRNN.pkl')
        
        playlist_quoted = [f"'{elem}'" for elem in playlist]
        sql_user_playlist = text(f'SELECT {", ".join("`"+col+"`" if col == "key" else col for col in audio_cols)} FROM song WHERE track_id IN ({", ".join(playlist_quoted)})')
        sql_all_audio_feats = text(f'SELECT track_id, {", ".join("`"+col+"`" if col == "key" else col for col in audio_cols)} FROM song WHERE track_id NOT IN ({", ".join(playlist_quoted)})')
        
        print(sql_user_playlist)
        session = db.session()
        try:
            cursor = session.execute(sql_user_playlist).cursor
            user_playlist_audio_feats = cursor.fetchall()
            cursor = session.execute(sql_all_audio_feats).cursor
            all_audio_feats = cursor.fetchall()
            print('%'*50)
            print(f'ALL AUDIO FEATURES: {len(all_audio_feats)} ')
            print(user_playlist_audio_feats)
            print('%'*50)
            for row in all_audio_feats:
                row = [float(x) if isinstance(x, Decimal) or isinstance(x, int) else x for x in row]
                master_audio_feats.append(row)

            for row in user_playlist_audio_feats:
                print(type(row))
                row = list(row)
                row = [float(x) if isinstance(x, Decimal) or isinstance(x, int) else x for x in row]
                print(type(row))
                print(row)
                input_seq.append(row)
        except Exception as e:
            print("Error executing query:", e)
            session.rollback()
        finally:
            session.close()
        
        print('^'*50)
        print(input_seq)
        print(len(input_seq))
        print('^'*50)

        # Converting input sequence into a 3D numpy array required for RNN model
        np_input_seq = np.array(input_seq)
        three_dim_input_seq = np.reshape(np_input_seq, (1, len(input_seq), 12))
        print(f'Three dimensional input sequence: {three_dim_input_seq}')

        # Pad the playlist to the optimal dimensions of (1, 35, 12)
        padded_playlist = pad_and_reshape(three_dim_input_seq)
        print(padded_playlist.shape)

        predictions = model.predict(padded_playlist)
        print('@'*50)
        print(predictions)
        print('@'*50)

        master_audio_feats = np.array(master_audio_feats)
        master_audio_feats[:, 1:].astype(np.float32)
        
        
        # calculate the cosine similarity between the input array and each row of the larger array
        cosine_similarites = np.apply_along_axis(lambda x: 1 - cosine(predictions, x), 1, master_audio_feats[:, 1:].astype(np.float32))
        most_similar_index = np.argsort(cosine_similarites[::-1][:5])
        print(f"Most similar row index(es): {most_similar_index}")
        
        for i in range(len(master_audio_feats)):
            if i in most_similar_index:
                recommended_track_ids.append(master_audio_feats[i, 0])
        
        print(recommended_track_ids)

        recommended_track_ids = [f"'{elem}'" for elem in recommended_track_ids]
        sql_recommended_track_ids = text(f'SELECT track_id, track_name, track_artist, track_album_name FROM song WHERE track_id IN ({", ".join(recommended_track_ids)})')

        try:
            cursor = session.execute(sql_recommended_track_ids).cursor
            recommended_tracks = cursor.fetchall()
        except Exception as e:
            print("Error executing query:", e)
            session.rollback()
        finally:
            session.close()
        print(type(recommended_tracks))
        recommended_tracks = list(recommended_tracks)
        print(recommended_tracks)

    return render_template("home.html", user=current_user, recommended_tracks=recommended_tracks)

@views.route('/songs', methods=['GET', 'POST'])
def display_songs():
    songs = Song.query
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
        'id', 'track_id', 'track_name', 'track_artist', 'lyrics', 'track_album_id' , 'playlist_name',
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