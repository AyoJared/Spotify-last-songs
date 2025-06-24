import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from app import app, db, Track

@pytest.fixture
def client():
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add(Track(id="track_2", name="Original", artist="Artist"))
        db.session.commit()
    with app.test_client() as client:
        yield client

def test_update_track(client):
    response = client.put("/tracks/track_2", json={"name": "Updated"})
    assert response.status_code == 200
    updated = client.get("/tracks").get_json()[0]
    assert updated["name"] == "Updated"

def test_delete_track(client):
    response = client.delete("/tracks/track_2")
    assert response.status_code == 200
    assert client.get("/tracks").get_json() == []
