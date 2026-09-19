import pytest
from app import create_app
from database.database import db
from database.models import User

@pytest.fixture()
def app():
    app = create_app()
    app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI="sqlite:///:memory:")
    with app.app_context():
        db.drop_all()
        db.create_all()
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

def test_register(client):
    response = client.post("/register", data={
        "name": "Test User", "email": "test@example.com", "password": "secret123"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Registration successful" in response.data

def test_login(client, app):
    client.post("/register", data={
        "name": "Test User", "email": "test@example.com", "password": "secret123"
    })
    response = client.post("/login", data={
        "email": "test@example.com", "password": "secret123"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Login successful" in response.data
