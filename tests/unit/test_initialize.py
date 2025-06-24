import sys
import os
import pytest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

@patch("app.get_spotify_tracks")  # ✅ patch where it's used, not where it's from
def test_initialize_database(mock_get_tracks):
    mock_get_tracks.return_value = [
        {"id": "mock123", "name": "Mock Song", "artist": "Mock Artist", "image_url": "mock_url"}
    ]

    from app import db, Track, initialize_database, app

    with app.app_context():
        db.drop_all()
        db.create_all()

        with patch.object(db.session, "get", return_value=None), \
             patch.object(db.session, "add") as mock_add, \
             patch.object(db.session, "commit") as mock_commit:

            initialize_database()
            assert mock_add.called
            assert mock_commit.called
