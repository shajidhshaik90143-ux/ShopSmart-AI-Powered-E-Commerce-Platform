from flask import Blueprint, jsonify, request
from database.models import Product
from ai.recommender import recommend_products

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/products")
def products_api():
    q = request.args.get("q", "").strip()
    query = Product.query.filter_by(is_active=True)
    if q:
        query = query.filter(Product.name.ilike(f"%{q}%"))
    products = query.limit(50).all()
    return jsonify([{
        "id": p.id, "name": p.name, "category": p.category,
        "price": p.price, "stock": p.stock, "rating": p.rating
    } for p in products])

@api_bp.route("/recommendations/<int:product_id>")
def recommendations_api(product_id):
    product = Product.query.get_or_404(product_id)
    products = Product.query.filter_by(is_active=True).all()
    recommendations = recommend_products(product, products)
    return jsonify([{
        "id": p.id, "name": p.name, "category": p.category, "price": p.price
    } for p in recommendations])
