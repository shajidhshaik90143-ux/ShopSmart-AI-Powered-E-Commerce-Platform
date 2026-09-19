from database.database import db
from database.models import CartItem

def cart_total(user_id):
    items = CartItem.query.filter_by(user_id=user_id).all()
    return sum(item.product.price * item.quantity for item in items)

def clear_cart(user_id):
    CartItem.query.filter_by(user_id=user_id).delete()
    db.session.commit()
