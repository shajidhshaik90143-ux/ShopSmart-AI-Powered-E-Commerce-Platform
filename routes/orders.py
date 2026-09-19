from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from routes.auth import login_required, current_user

from database.database import db

from database.models import (
    CartItem,
    Order,
    OrderItem,
    Sale,
    Product
)

from services.payment_service import process_payment

from services.notification_service import (
    send_order_notification
)

from ai.fraud_detection import fraud_score


orders_bp = Blueprint(
    "orders",
    __name__,
    url_prefix="/orders"
)


def get_cart_items():

    return CartItem.query.filter_by(
        user_id=current_user().id
    ).all()


def calculate_total(items):

    return sum(
        item.product.price * item.quantity
        for item in items
    )


# ------------------------------------------------
# MY ORDERS
# ------------------------------------------------

@orders_bp.route("/")
@login_required
def list_orders():

    orders = (
        Order.query
        .filter_by(user_id=current_user().id)
        .order_by(Order.created_at.desc())
        .all()
    )

    return render_template(
        "orders.html",
        orders=orders
    )


# ------------------------------------------------
# BUY NOW
# ------------------------------------------------

@orders_bp.route(
    "/buy-now/<int:product_id>"
)
@login_required
def buy_now(product_id):

    product = db.get_or_404(
        Product,
        product_id
    )

    if not product.is_active:

        flash(
            "This product is unavailable.",
            "danger"
        )

        return redirect(
            url_for(
                "products.list_products"
            )
        )

    if product.stock <= 0:

        flash(
            "This product is out of stock.",
            "danger"
        )

        return redirect(
            url_for(
                "products.product_detail",
                product_id=product.id
            )
        )

    # Clear existing cart
    CartItem.query.filter_by(
        user_id=current_user().id
    ).delete()

    # Add selected product
    item = CartItem(
        user_id=current_user().id,
        product_id=product.id,
        quantity=1
    )

    db.session.add(item)

    db.session.commit()

    return redirect(
        url_for(
            "orders.checkout"
        )
    )


# ------------------------------------------------
# CHECKOUT
# ------------------------------------------------

@orders_bp.route(
    "/checkout",
    methods=["GET", "POST"]
)
@login_required
def checkout():

    items = get_cart_items()

    if not items:

        flash(
            "Your cart is empty.",
            "warning"
        )

        return redirect(
            url_for("cart.view_cart")
        )

    # Check stock
    for item in items:

        if item.product.stock < item.quantity:

            flash(
                f"Only {item.product.stock} "
                f"unit(s) of "
                f"{item.product.name} "
                f"are available.",
                "danger"
            )

            return redirect(
                url_for("cart.view_cart")
            )

    total = calculate_total(items)

    # ------------------------------------------------
    # POST CHECKOUT
    # ------------------------------------------------

    if request.method == "POST":

        address = request.form.get(
            "address",
            ""
        ).strip()

        payment_method = request.form.get(
            "payment_method",
            "online"
        ).lower()

        # Address validation
        if len(address) < 10:

            flash(
                "Please enter a complete shipping address.",
                "danger"
            )

            return render_template(
                "checkout.html",
                items=items,
                total=total
            )

        # Payment validation
        if payment_method not in {
            "online",
            "cod"
        }:

            flash(
                "Invalid payment method.",
                "danger"
            )

            return render_template(
                "checkout.html",
                items=items,
                total=total
            )

        # Fraud check
        risk = fraud_score(
            current_user(),
            items,
            total
        )

        if risk >= 90:

            flash(
                "Order was held for security review.",
                "danger"
            )

            return render_template(
                "checkout.html",
                items=items,
                total=total
            )

        # ------------------------------------------------
        # ONLINE PAYMENT
        # ------------------------------------------------

        if payment_method == "online":

            payment = process_payment(
                total
            )

            if not payment["success"]:

                flash(
                    "Online payment failed.",
                    "danger"
                )

                return render_template(
                    "checkout.html",
                    items=items,
                    total=total
                )

            payment_status = "Paid"

            selected_payment_method = (
                "Online Payment"
            )

            payment_id = payment[
                "transaction_id"
            ]

        # ------------------------------------------------
        # CASH ON DELIVERY
        # ------------------------------------------------

        else:

            payment_status = "Pending"

            selected_payment_method = (
                "Cash on Delivery"
            )

            payment_id = None

        # ------------------------------------------------
        # FINAL STOCK CHECK
        # ------------------------------------------------

        for item in items:

            if item.quantity > item.product.stock:

                db.session.rollback()

                flash(
                    f"Insufficient stock for "
                    f"{item.product.name}.",
                    "danger"
                )

                return redirect(
                    url_for(
                        "cart.view_cart"
                    )
                )

        # ------------------------------------------------
        # CREATE ORDER
        # ------------------------------------------------

        order = Order(

            user_id=current_user().id,

            total_amount=total,

            shipping_address=address,

            payment_status=payment_status,

            payment_method=(
                selected_payment_method
            ),

            payment_id=payment_id,

            status="Placed"
        )

        db.session.add(order)

        db.session.flush()

        # ------------------------------------------------
        # CREATE ORDER ITEMS
        # ------------------------------------------------

        for item in items:

            # Reduce stock
            item.product.stock -= (
                item.quantity
            )

            # Order item
            db.session.add(
                OrderItem(

                    order_id=order.id,

                    product_id=item.product.id,

                    product_name=item.product.name,

                    price=item.product.price,

                    quantity=item.quantity
                )
            )

            # Sales record
            db.session.add(
                Sale(

                    product_id=item.product.id,

                    quantity=item.quantity,

                    amount=(
                        item.product.price
                        * item.quantity
                    )
                )
            )

            # Remove cart item
            db.session.delete(item)

        db.session.commit()

        # Notification
        send_order_notification(
            current_user().email,
            order.id
        )

        flash(
            f"Order #{order.id} placed successfully.",
            "success"
        )

        return redirect(
            url_for(
                "orders.order_success",
                order_id=order.id
            )
        )

    # GET request
    return render_template(
        "checkout.html",
        items=items,
        total=total
    )


# ------------------------------------------------
# ORDER SUCCESS
# ------------------------------------------------

@orders_bp.route(
    "/success/<int:order_id>"
)
@login_required
def order_success(order_id):

    order = db.get_or_404(
        Order,
        order_id
    )

    if (
        order.user_id != current_user().id
        and not current_user().is_admin
    ):

        flash(
            "You cannot view this order.",
            "danger"
        )

        return redirect(
            url_for(
                "orders.list_orders"
            )
        )

    return render_template(
        "order_success.html",
        order=order
    )


# ------------------------------------------------
# ORDER DETAILS
# ------------------------------------------------

@orders_bp.route(
    "/<int:order_id>"
)
@login_required
def detail(order_id):

    order = db.get_or_404(
        Order,
        order_id
    )

    if (
        order.user_id != current_user().id
        and not current_user().is_admin
    ):

        flash(
            "You cannot view this order.",
            "danger"
        )

        return redirect(
            url_for(
                "orders.list_orders"
            )
        )

    return render_template(
        "orders.html",
        orders=[order],
        detail_mode=True
    )