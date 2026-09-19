from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from database.database import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(120),
        nullable=False
    )

    email = db.Column(
        db.String(160),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    is_admin = db.Column(
        db.Boolean,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    cart_items = db.relationship(
        "CartItem",
        backref="user",
        cascade="all, delete-orphan"
    )

    wishlist_items = db.relationship(
        "WishlistItem",
        backref="user",
        cascade="all, delete-orphan"
    )

    orders = db.relationship(
        "Order",
        backref="user",
        cascade="all, delete-orphan"
    )

    reviews = db.relationship(
        "Review",
        backref="user",
        cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(
            self.password_hash,
            password
        )


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(180),
        nullable=False,
        index=True
    )

    category = db.Column(
        db.String(100),
        nullable=False,
        index=True
    )

    description = db.Column(
        db.Text,
        default=""
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    stock = db.Column(
        db.Integer,
        default=0
    )

    image_url = db.Column(
        db.String(500),
        default=""
    )

    rating = db.Column(
        db.Float,
        default=0.0
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    cart_items = db.relationship(
        "CartItem",
        backref="product",
        cascade="all, delete-orphan"
    )

    wishlist_items = db.relationship(
        "WishlistItem",
        backref="product",
        cascade="all, delete-orphan"
    )

    reviews = db.relationship(
        "Review",
        backref="product",
        cascade="all, delete-orphan"
    )


class CartItem(db.Model):
    __tablename__ = "cart_items"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        default=1
    )

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "product_id",
            name="uq_cart_user_product"
        ),
    )


class WishlistItem(db.Model):
    __tablename__ = "wishlist_items"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "product_id",
            name="uq_wishlist_user_product"
        ),
    )


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    total_amount = db.Column(
        db.Float,
        nullable=False
    )

    status = db.Column(
        db.String(40),
        default="Placed"
    )

    payment_status = db.Column(
        db.String(40),
        default="Pending"
    )

    payment_method = db.Column(
        db.String(40),
        default="Online Payment"
    )

    payment_id = db.Column(
        db.String(200),
        nullable=True
    )

    shipping_address = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    items = db.relationship(
        "OrderItem",
        backref="order",
        cascade="all, delete-orphan"
    )


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    order_id = db.Column(
        db.Integer,
        db.ForeignKey("orders.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=True
    )

    product_name = db.Column(
        db.String(180),
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    rating = db.Column(
        db.Integer,
        nullable=False
    )

    comment = db.Column(
        db.Text,
        nullable=False
    )

    sentiment = db.Column(
        db.String(30),
        default="neutral"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


class Sale(db.Model):
    __tablename__ = "sales"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    amount = db.Column(
        db.Float,
        nullable=False
    )

    sale_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )