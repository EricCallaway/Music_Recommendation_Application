from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #This is an example of a foreign key


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')

class Song(db.Model):
    __tablename__ = 'song'
    id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.String(150), unique=True, nullable=False)
    track_name = db.Column(db.String(150), nullable=False)
    track_artist = db.Column(db.String(150), nullable=False)
    lyrics = db.Column(db.Text)
    track_album_id = db.Column(db.String(150), unique=False, nullable=False)
    track_album_name = db.Column(db.String(150), nullable=False)
    playlist_name = db.Column(db.String(150), nullable=False)
    playlist_id = db.Column(db.String(150), unique=False, nullable=False)
    playlist_genre = db.Column(db.String(150), nullable=False)
    playlist_subgenre = db.Column(db.String(150), nullable=False)
    danceability = db.Column(db.Numeric(10,3), nullable=False)
    energy = db.Column(db.Numeric(10,4), nullable=False)
    key = db.Column(db.Integer, nullable=False)
    loudness = db.Column(db.Numeric(10,4), nullable=False)
    mode = db.Column(db.Integer, nullable=False)
    speechiness = db.Column(db.Numeric(10,4), nullable=False)
    acousticness = db.Column(db.Numeric(10,5), nullable=False)
    instrumentalness = db.Column(db.Numeric(10,5), nullable=False)
    liveness = db.Column(db.Numeric(10,5), nullable=False)
    valence = db.Column(db.Numeric(10,4), nullable=False)
    tempo = db.Column(db.Numeric(10,3), nullable=False)
    duration_ms = db.Column(db.Integer, nullable=False)
    language = db.Column(db.String(10))

    def to_dict(self):
        return {
            'id' : self.id,
            'track_id' : self.track_id,
            'track_name': self.track_name,
            'track_artist': self.track_artist,
            'lyrics': self.lyrics,
            'track_album_id': self.track_album_id,
            'track_album_name': self.track_album_name,
            'playlist_name': self.playlist_name,
            'playlist_id': self.playlist_id,
            'playlist_genre': self.playlist_genre,
            'playlist_subgenre': self.playlist_subgenre,
            'danceability': self.danceability,
            'energy': self.energy,
            'key': self.key,
            'loudness': self.loudness,
            'mode': self.mode,
            'speechiness': self.speechiness,
            'acousticness': self.acousticness,
            'instrumentalness': self.instrumentalness,
            'liveness': self.liveness,
            'valence': self.valence,
            'tempo': self.tempo,
            'duration_ms': self.duration_ms,
            'language': self.language
        }
    
class Billboard(db.Model):
    __tablename__ = 'billboard'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True))
    title = db.Column(db.String(150), unique=True, nullable=False)
    artist = db.Column(db.String(150), nullable=False)
    spotify_link = db.Column(db.String(150), nullable=False)
    spotify_id = db.Column(db.String(150), unique=True, nullable=False)
    genre = db.Column(db.String(150), nullable=False)
    analysis_url = db.Column(db.String(150), nullable=False)
    energy = db.Column(db.Numeric(10,4), nullable=False)
    liveness = db.Column(db.Numeric(10,5), nullable=False)
    tempo = db.Column(db.Numeric(10,3), nullable=False)
    speechiness = db.Column(db.Numeric(10,4), nullable=False)
    acousticness = db.Column(db.Numeric(10,5), nullable=False)
    instrumentalness = db.Column(db.Numeric(10,5), nullable=False)
    time_signature = db.Column(db.Numeric(10,5), nullable=False)
    danceability = db.Column(db.Numeric(10, 3), nullable=False)
    key = db.Column(db.Integer, nullable=False)
    duration_ms = db.Column(db.Integer, nullable=False)
    loudness = db.Column(db.Numeric(10,4), nullable=False)
    valence = db.Column(db.Numeric(10,4), nullable=False)
    mode = db.Column(db.Integer, nullable=False)
    lyrics = db.Column(db.String(1000))
    clean_lyrics = db.Column(db.String(1000))

    def to_dict(self):
        return {
            'id' : self.id,
            'date' : self.date,
            'title': self.title,
            'artist': self.artist,
            'spotify_link': self.spotify_link,
            'spotify_id': self.spotify_id,
            'genre': self.genre,
            'analysis_url': self.analysis_url,
            'energy': self.energy,
            'liveness': self.liveness,
            'tempo': self.tempo,
            'speechiness': self.speechiness,
            'acousticness': self.acousticness,
            'instrumentalness': self.instrumentalness,
            'time_signature': self.time_signature,
            'danceability': self.danceability,
            'key': self.key,
            'duration_ms': self.duration_ms,
            'loudness': self.loudness,
            'valence': self.valence,
            'mode': self.mode,
            'lyrics': self.lyrics,
            'clean_lyrics': self.clean_lyrics,
        } 
    

    
class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    age = db.Column(db.String(150))

    def to_dict(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'age' : self.age
        }
    
        