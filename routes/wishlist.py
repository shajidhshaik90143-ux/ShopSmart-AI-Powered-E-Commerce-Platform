from flask import Blueprint, render_template, redirect, url_for, flash
from routes.auth import login_required, current_user
from database.database import db
from database.models import Product, WishlistItem

wishlist_bp = Blueprint("wishlist", __name__, url_prefix="/wishlist")

@wishlist_bp.route("/")
@login_required
def view():
    items = WishlistItem.query.filter_by(user_id=current_user().id).all()
    return render_template("wishlist.html", items=items)

@wishlist_bp.route("/toggle/<int:product_id>", methods=["POST", "GET"])
@login_required
def toggle(product_id):
    db.get_or_404(Product, product_id)
    item = WishlistItem.query.filter_by(
        user_id=current_user().id, product_id=product_id
    ).first()
    if item:
        db.session.delete(item)
        flash("Removed from wishlist.", "info")
    else:
        db.session.add(WishlistItem(user_id=current_user().id, product_id=product_id))
        flash("Added to wishlist.", "success")
    db.session.commit()
    return redirect(url_for("wishlist.view"))
