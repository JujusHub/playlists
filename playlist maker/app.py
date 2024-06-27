from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///songs.db'
db = SQLAlchemy(app)

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    songs = db.relationship('Song', backref='playlist', lazy=True)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'), nullable=False)

db.create_all()


class SongForm(FlaskForm):
    title = StringField('Song Title', validators=[DataRequired()])
    artist = StringField('Artist', validators=[DataRequired()])
    playlist_name = StringField('Playlist', validators=[DataRequired()])
    submit = SubmitField('Add Song')




@app.route('/', methods=['GET', 'POST'])
def index():
    form = SongForm()
    if form.validate_on_submit():
        playlist_name = form.playlist_name.data
        playlist = Playlist.query.filter_by(name=playlist_name).first()
        if not playlist:
            playlist = Playlist(name=playlist_name)
            db.session.add(playlist)
            db.session.commit()
        
        song = Song(title=form.title.data, artist=form.artist.data, playlist=playlist)
        db.session.add(song)
        db.session.commit()
        return redirect(url_for('index'))
    
    playlists = Playlist.query.all()
    return render_template('index.html', form=form, playlists=playlists)

if __name__ == '__main__':
    app.run(debug=True)
