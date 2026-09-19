from datetime import datetime, timedelta
from app import app
from database.database import db
from database.models import User, Product, Review, Sale

PRODUCTS = [
    ("Wireless Headphones", "Electronics", "Bluetooth over-ear headphones with clear sound and long battery life.", 2499, 35),
    ("Smart Watch", "Electronics", "Fitness-focused smartwatch with heart-rate tracking and notifications.", 3299, 22),
    ("Mechanical Keyboard", "Computers", "Compact mechanical keyboard for coding and gaming.", 2899, 18),
    ("Laptop Backpack", "Accessories", "Water-resistant backpack with a padded laptop compartment.", 1499, 40),
    ("Running Shoes", "Fashion", "Lightweight running shoes designed for everyday training.", 2199, 27),
    ("Cotton T-Shirt", "Fashion", "Comfortable regular-fit cotton T-shirt.", 699, 80),
    ("Coffee Maker", "Home", "Automatic coffee maker with reusable filter.", 3799, 12),
    ("Study Lamp", "Home", "LED desk lamp with adjustable brightness.", 999, 50),
    ("Power Bank", "Electronics", "10000mAh fast-charging power bank.", 1299, 31),
    ("Bluetooth Speaker", "Electronics", "Portable wireless speaker with deep bass.", 1799, 25),
    ("Notebook Set", "Books", "Premium ruled notebooks for college and office use.", 449, 100),
    ("USB-C Hub", "Computers", "Multi-port USB-C hub for laptops.", 1699, 20),
]

def seed():
    with app.app_context():
        db.drop_all()
        db.create_all()

        admin = User(name="Admin", email="admin@shopsmart.com", is_admin=True)
        admin.set_password("Admin@123")
        user = User(name="Demo User", email="user@shopsmart.com")
        user.set_password("User@123")
        db.session.add_all([admin, user])
        db.session.flush()

        products = []
        for name, category, desc, price, stock in PRODUCTS:
            p = Product(
                name=name, category=category, description=desc,
                price=price, stock=stock,
                image_url=f"https://picsum.photos/seed/{name.replace(' ', '')}/700/500"
            )
            products.append(p)
            db.session.add(p)
        db.session.flush()

        comments = [
            ("Great product and excellent quality.", 5),
            ("Good value for money.", 4),
            ("The product is okay but delivery was slow.", 3),
            ("Amazing quality, I really like it.", 5),
        ]
        for i, p in enumerate(products[:4]):
            comment, rating = comments[i]
            db.session.add(Review(
                user_id=user.id, product_id=p.id, rating=rating,
                comment=comment, sentiment="positive"
            ))

        for day in range(30):
            for p in products[:6]:
                qty = ((day + p.id) % 5) + 1
                db.session.add(Sale(
                    product_id=p.id,
                    quantity=qty,
                    amount=qty * p.price,
                    sale_date=datetime.utcnow() - timedelta(days=29-day)
                ))

        db.session.commit()
        print("Database seeded successfully.")
        print("Admin: admin@shopsmart.com / Admin@123")
        print("User:  user@shopsmart.com / User@123")

if __name__ == "__main__":
    seed()
