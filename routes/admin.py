from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import func
from routes.auth import admin_required
from database.database import db
from database.models import User, Product, Order, Sale
from ai.sales_prediction import predict_next_sales

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/")
@admin_required
def dashboard():
    revenue = db.session.query(func.coalesce(func.sum(Order.total_amount), 0)).scalar()
    data = {
        "users": User.query.count(),
        "products": Product.query.count(),
        "orders": Order.query.count(),
        "revenue": float(revenue or 0),
        "low_stock": Product.query.filter(Product.stock <= 5, Product.is_active == True).count()
    }
    prediction = predict_next_sales()
    return render_template("admin/dashboard.html", data=data, prediction=prediction)

@admin_bp.route("/products", methods=["GET", "POST"])
@admin_required
def products():
    if request.method == "POST":
        p = Product(
            name=request.form.get("name", "").strip(),
            category=request.form.get("category", "General").strip(),
            description=request.form.get("description", "").strip(),
            price=float(request.form.get("price", 0)),
            stock=int(request.form.get("stock", 0)),
            image_url=request.form.get("image_url", "").strip()
        )
        if not p.name or p.price < 0 or p.stock < 0:
            flash("Invalid product data.", "danger")
            return redirect(url_for("admin.products"))
        db.session.add(p)
        db.session.commit()
        flash("Product created.", "success")
    products = Product.query.order_by(Product.id.desc()).all()
    return render_template("admin/products.html", products=products)

@admin_bp.route("/products/delete/<int:product_id>", methods=["POST"])
@admin_required
def delete_product(product_id):
    p = db.get_or_404(Product, product_id)
    p.is_active = False
    db.session.commit()
    flash("Product deactivated.", "success")
    return redirect(url_for("admin.products"))

@admin_bp.route("/users")
@admin_required
def users():
    return render_template("admin/users.html", users=User.query.order_by(User.id.desc()).all())

@admin_bp.route("/orders")
@admin_required
def orders():
    return render_template("admin/orders.html", orders=Order.query.order_by(Order.created_at.desc()).all())

@admin_bp.route("/orders/<int:order_id>/status", methods=["POST"])
@admin_required
def update_order_status(order_id):
    order = db.get_or_404(Order, order_id)
    status = request.form.get("status", "Placed")
    allowed = {"Placed", "Processing", "Shipped", "Delivered", "Cancelled"}
    if status in allowed:
        order.status = status
        db.session.commit()
        flash("Order status updated.", "success")
    return redirect(url_for("admin.orders"))

@admin_bp.route("/inventory")
@admin_required
def inventory():
    products = Product.query.order_by(Product.stock.asc()).all()
    return render_template("admin/inventory.html", products=products)

@admin_bp.route("/analytics")
@admin_required
def analytics():
    sales = Sale.query.order_by(Sale.sale_date.desc()).limit(100).all()
    return render_template("admin/analytics.html", sales=sales)
