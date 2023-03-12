from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .models import Note, Song, User, Pet
from . import db 
import json
import joblib

#Creating blueprint named "views"
views = Blueprint('views', __name__)

def recommend_songs(playlist):
    # Load the previously trained model
    model = joblib.load('../../../training_model/model_testing.ipynb')

    # Use the model to make predictions on the playlist
    predictions = model.predict(playlist)

    # Return the predictions 
    return predictions

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        playlist = []
        for i in range(len(request.form)):
            song = request.form.get(f'song{i}')
            if song:
                playlist.append(song)
        print('$'*50)
        print(playlist)
        print('$'*50)
        print(len(request.form))

    return render_template("home.html", user=current_user)

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