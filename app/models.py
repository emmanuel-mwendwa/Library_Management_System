from . import db, login_manager

from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime, timedelta

from flask_login import UserMixin

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(16), nullable=False)
    last_name = db.Column(db.String(16), nullable=False)
    email = db.Column(db.String(56), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(76), nullable=False)
    member_since = db.Column(db.DateTime, default=datetime.now())

    @property
    def password(self):
        raise AttributeError('Cannot read password.')
    
    @password.setter
    def password(self, password):

        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):

        return check_password_hash(self.password_hash, password)
    

# function to load a user from the database
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    

class Book(db.Model):

    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    publication_date = db.Column(db.Date, nullable=True)
    isbn = db.Column(db.String(20), unique=True, nullable=True)
    available_copies = db.Column(db.Integer, default=1)
    total_copies = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
