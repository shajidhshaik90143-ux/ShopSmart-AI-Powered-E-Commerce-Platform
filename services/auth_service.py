from database.models import User
from database.database import db

def authenticate(email, password):
    user = User.query.filter_by(email=email.lower().strip()).first()
    return user if user and user.check_password(password) else None

def create_user(name, email, password):
    user = User(name=name.strip(), email=email.lower().strip())
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user
