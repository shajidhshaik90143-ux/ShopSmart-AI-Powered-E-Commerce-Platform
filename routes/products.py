from flask import Blueprint, render_template, request
from database.models import Product
from database.database import db

products_bp = Blueprint("products", __name__, url_prefix="/products")

@products_bp.route("/")
def list_products():
    q = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()
    query = Product.query.filter_by(is_active=True)
    if q:
        query = query.filter(
            db.or_(
                Product.name.ilike(f"%{q}%"),
                Product.description.ilike(f"%{q}%")
            )
        )
    if category:
        query = query.filter_by(category=category)
    products = query.order_by(Product.created_at.desc()).all()
    categories = [r[0] for r in db.session.query(Product.category).distinct().all()]
    return render_template("products.html", products=products, categories=categories, q=q, category=category)

@products_bp.route("/<int:product_id>")
def product_detail(product_id):
    product = db.get_or_404(Product, product_id)
    return render_template("product.html", product=product)
