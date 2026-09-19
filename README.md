# ShopSmart - AI E-Commerce Platform

ShopSmart is a Flask-based e-commerce application with:

- User registration/login/logout
- Product catalog and search
- Product detail pages
- Cart and quantity management
- Wishlist
- Checkout and mock payment
- Orders and order history
- Product reviews with sentiment analysis
- AI-style recommendations
- Sales prediction
- Basic fraud-risk detection
- Rule-based shopping assistant
- Admin dashboard
- Product, user, order and inventory management
- Analytics
- JSON API
- Pytest tests

## 1. Create environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 2. Seed database

```powershell
python -m database.seed
```

This creates sample products, users and reviews.

Demo accounts:

- Admin: admin@shopsmart.com / Admin@123
- User: user@shopsmart.com / User@123

## 3. Run

```powershell
python app.py
```

Open:

http://127.0.0.1:5000

## Notes

The payment system is intentionally a mock payment service. Do not store real card numbers.
The AI modules use local algorithms so the project works without a paid AI API.
