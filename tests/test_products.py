import pytest
from app import create_app
from database.database import db
from database.models import Product

@pytest.fixture()
def app():
    app = create_app()
    app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI="sqlite:///:memory:")
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.add(Product(name="Test Phone", category="Electronics", description="Phone", price=100, stock=5))
        db.session.commit()
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

def test_products_page(client):
    response = client.get("/products/")
    assert response.status_code == 200
    assert b"Test Phone" in response.data

def test_product_api(client):
    response = client.get("/api/products?q=Phone")
    assert response.status_code == 200
    assert response.json[0]["name"] == "Test Phone"
