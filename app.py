from flask import Flask, render_template, redirect, url_for
from config import Config
from database.database import db
from database.models import User
from routes.auth import auth_bp
from routes.products import products_bp
from routes.cart import cart_bp
from routes.wishlist import wishlist_bp
from routes.orders import orders_bp
from routes.reviews import reviews_bp
from routes.admin import admin_bp
from routes.api import api_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(wishlist_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def index():
        from database.models import Product
        products = Product.query.filter_by(is_active=True).order_by(Product.created_at.desc()).limit(8).all()
        return render_template("index.html", products=products)

    @app.errorhandler(404)
    def not_found(error):
        return render_template("base.html", content_title="Page not found",
                               content_message="The requested page does not exist."), 404

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
