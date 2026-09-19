from flask import Blueprint, request, redirect, url_for, flash
from routes.auth import login_required, current_user
from database.database import db
from database.models import Product, Review
from ai.sentiment import analyze_sentiment

reviews_bp = Blueprint("reviews", __name__, url_prefix="/reviews")

@reviews_bp.route("/add/<int:product_id>", methods=["POST"])
@login_required
def add(product_id):
    product = db.get_or_404(Product, product_id)
    try:
        rating = int(request.form.get("rating", 5))
    except ValueError:
        rating = 5
    rating = max(1, min(5, rating))
    comment = request.form.get("comment", "").strip()
    if len(comment) < 3:
        flash("Review is too short.", "danger")
        return redirect(url_for("products.product_detail", product_id=product.id))

    existing = Review.query.filter_by(
        user_id=current_user().id, product_id=product.id
    ).first()
    if existing:
        existing.rating = rating
        existing.comment = comment
        existing.sentiment = analyze_sentiment(comment)
    else:
        db.session.add(Review(
            user_id=current_user().id,
            product_id=product.id,
            rating=rating,
            comment=comment,
            sentiment=analyze_sentiment(comment)
        ))

    reviews = Review.query.filter_by(product_id=product.id).all()
    product.rating = round(sum(r.rating for r in reviews) / len(reviews), 2)
    db.session.commit()
    flash("Review saved.", "success")
    return redirect(url_for("products.product_detail", product_id=product.id))
