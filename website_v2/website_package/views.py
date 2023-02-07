from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .models import Note, Song, User
from . import db 
import json

#Creating blueprint named "views"
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)

#takes string from js function and makes it a python function
@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

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
def data():
    return {'data' : [song.to_dict() for song in Song.query]}

