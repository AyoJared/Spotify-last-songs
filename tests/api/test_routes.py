import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from app import app, db, Track

@pytest.fixture
def client():
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add(Track(id="2", name="Test", artist="Tester"))
        db.session.commit()
    with app.test_client() as client:
        yield client

def test_update_track(client):
    response = client.put("/tracks/2", json={"name": "Updated"})
    assert response.status_code == 200
    data = client.get("/tracks").get_json()
    assert data[0]["name"] == "Updated"

def test_delete_track(client):
    response = client.delete("/tracks/2")
    assert response.status_code == 200
    data = client.get("/tracks").get_json()
    assert data == []
