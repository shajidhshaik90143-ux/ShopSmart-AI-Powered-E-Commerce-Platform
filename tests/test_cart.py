import pytest
from app import create_app
from database.database import db
from database.models import User, Product

@pytest.fixture()
def app():
    app = create_app()
    app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI="sqlite:///:memory:")
    with app.app_context():
        db.drop_all()
        db.create_all()
        user = User(name="User", email="user@test.com")
        user.set_password("secret123")
        db.session.add(user)
        db.session.add(Product(name="Mouse", category="Computers", description="Mouse", price=500, stock=10))
        db.session.commit()
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

def login(client):
    client.post("/login", data={"email":"user@test.com","password":"secret123"})

def test_add_to_cart(client):
    login(client)
    response = client.post("/cart/add/1", follow_redirects=True)
    assert response.status_code == 200
    assert b"Mouse" in response.data
