import pytest
from app import create_app
from database.database import db
from database.models import User, Product, CartItem

@pytest.fixture()
def app():
    app = create_app()
    app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI="sqlite:///:memory:")
    with app.app_context():
        db.drop_all()
        db.create_all()
        user = User(name="User", email="user@test.com")
        user.set_password("secret123")
        product = Product(name="Book", category="Books", description="Book", price=200, stock=10)
        db.session.add_all([user, product])
        db.session.commit()
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

def test_checkout(client, app):
    client.post("/login", data={"email":"user@test.com","password":"secret123"})
    client.post("/cart/add/1")
    response = client.post("/orders/checkout", data={
        "address": "123 Main Street, Ongole, Andhra Pradesh"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"placed successfully" in response.data
