from flask import Blueprint, render_template, request, redirect, url_for, flash
from routes.auth import login_required, current_user
from database.database import db
from database.models import Product, CartItem

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")

def get_items():
    return CartItem.query.filter_by(user_id=current_user().id).all()

@cart_bp.route("/")
@login_required
def view_cart():
    items = get_items()
    total = sum(i.product.price * i.quantity for i in items)
    return render_template("cart.html", items=items, total=total)

@cart_bp.route("/add/<int:product_id>", methods=["POST", "GET"])
@login_required
def add(product_id):
    product = db.get_or_404(Product, product_id)
    if product.stock <= 0:
        flash("Product is out of stock.", "danger")
        return redirect(request.referrer or url_for("products.list_products"))
    item = CartItem.query.filter_by(user_id=current_user().id, product_id=product.id).first()
    if item:
        if item.quantity < product.stock:
            item.quantity += 1
    else:
        db.session.add(CartItem(user_id=current_user().id, product_id=product.id, quantity=1))
    db.session.commit()
    flash("Product added to cart.", "success")
    return redirect(request.referrer or url_for("cart.view_cart"))

@cart_bp.route("/update/<int:item_id>", methods=["POST"])
@login_required
def update(item_id):
    item = db.get_or_404(CartItem, item_id)
    if item.user_id != current_user().id:
        flash("Invalid cart item.", "danger")
        return redirect(url_for("cart.view_cart"))
    try:
        qty = max(1, int(request.form.get("quantity", 1)))
    except ValueError:
        qty = 1
    item.quantity = min(qty, item.product.stock)
    db.session.commit()
    return redirect(url_for("cart.view_cart"))

@cart_bp.route("/remove/<int:item_id>", methods=["POST"])
@login_required
def remove(item_id):
    item = db.get_or_404(CartItem, item_id)
    if item.user_id == current_user().id:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for("cart.view_cart"))
