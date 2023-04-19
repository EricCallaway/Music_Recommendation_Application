from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    
class Billboard(db.Model):
    __tablename__ = 'billboard'
    date = db.Column(db.DateTime(timezone=True))
    title = db.Column(db.String(150), unique=True, nullable=False)
    artist = db.Column(db.String(150), nullable=False)
    spotify_link = db.Column(db.String(150), nullable=False)
    spotify_id = db.Column(db.String(150), unique=True, nullable=False, primary_key=True)
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