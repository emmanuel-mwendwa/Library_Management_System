from . import db

from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime, timedelta

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(16), nullable=False)
    last_name = db.Column(db.String(16), nullable=False)
    email = db.Column(db.String(56), nullable=False)
    password_hash = db.Column(db.String(76))
    member_since = db.Column(db.DateTime, default=datetime.now())

    @property
    def password(self):
        raise AttributeError('Cannot read password.')
    
    @password.setter
    def password(self, password):

        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):

        return check_password_hash(self.password_hash, password)
    
