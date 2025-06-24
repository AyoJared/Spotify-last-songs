from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from getsTheMostPopularSongs import get_spotify_tracks
from sqlalchemy import inspect
import os
import time
import sqlalchemy.exc

app = Flask(__name__)

# PostgreSQL config from env (Docker Compose)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASS']}"
    f"@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Track(db.Model):
    __tablename__ = 'tracks'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    artist = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String)

@app.route("/")
def home():
    tracks = Track.query.all()
    return render_template("index.html", tracks=tracks)

@app.route("/tracks", methods=["GET"])
def get_tracks():
    return jsonify([
        {
            "id": t.id,
            "name": t.name,
            "artist": t.artist,
            "image_url": t.image_url
        }
        for t in Track.query.all()
    ])

@app.route("/tracks", methods=["POST"])
def add_track():
    data = request.json
    if not data or not all(k in data for k in ("id", "name", "artist")):
        return jsonify({"error": "Missing track data"}), 400
    if Track.query.get(data["id"]):
        return jsonify({"error": "Track ID already exists"}), 409
    new_track = Track(
        id=data["id"],
        name=data["name"],
        artist=data["artist"],
        image_url=data.get("image_url")
    )
    db.session.add(new_track)
    db.session.commit()
    return jsonify({"message": "Track added"}), 201

@app.route("/tracks/<id>", methods=["PUT"])
def update_track(id):
    track = db.session.get(Track, id)    
    if not track:
        return jsonify({"error": "Track not found"}), 404
    data = request.json
    track.name = data.get("name", track.name)
    track.artist = data.get("artist", track.artist)
    track.image_url = data.get("image_url", track.image_url)
    db.session.commit()
    return jsonify({"message": "Track updated"})

@app.route("/tracks/<id>", methods=["DELETE"])
def delete_track(id):
    track = db.session.get(Track, id)    
    if not track:
        return jsonify({"error": "Track not found"}), 404
    db.session.delete(track)
    db.session.commit()
    return jsonify({"message": "Track deleted"})

def initialize_database():
    with app.app_context():
        print("🔧 Initializing database...")
        db.create_all()
        inspector = inspect(db.engine)
        print("📦 Current tables:", inspector.get_table_names())

        if not Track.query.first():
            print("🎧 Preloading Spotify tracks...")
            for track in get_spotify_tracks():
                if not Track.query.get(track["id"]):
                    db.session.add(Track(
                        id=track["id"],
                        name=track["name"],
                        artist=track["artist"],
                        image_url=track.get("image_url")
                    ))
            db.session.commit()
            print("✅ Tracks loaded.")
        else:
            print("📚 Tracks already exist — skipping preload.")

if __name__ == "__main__":
    initialize_database()
    app.run(host="0.0.0.0", port=3000, debug=True)