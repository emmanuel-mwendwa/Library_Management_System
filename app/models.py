from . import db, login_manager

from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime, timedelta

from flask_login import UserMixin

from sqlalchemy.orm import backref

class CRUDMixin:

    @classmethod
    def create(cls, **kwargs):
        """Create a new record."""
        instance = cls(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance

    @classmethod
    def get(cls, id):
        """Get a record by its primary key."""
        return cls.query.get(id)

    def update(self, commit=True, **kwargs):
        """Update the attributes of the instance."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Delete the record from the database."""
        db.session.delete(self)
        if commit:
            db.session.commit()

    @classmethod
    def get_all(cls):
        """Get all records."""
        return cls.query.all()


class User(UserMixin, db.Model, CRUDMixin):

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
    

class Book(db.Model, CRUDMixin):

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

    transactions = db.relationship('Transaction', backref=backref('book'), lazy=True)


class Member(db.Model, CRUDMixin):

    __tablename__ = "members"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(16), nullable=False)
    last_name = db.Column(db.String(16), nullable=False)
    email = db.Column(db.String(56), unique=True, index=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    transactions = db.relationship('Transaction', backref=backref('member'), lazy=True)

class Transaction(db.Model, CRUDMixin):

    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id', ondelete='CASCADE'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id', ondelete='CASCADE'), nullable=False)
    issue_date = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, nullable=True)
    rent_fee = db.Column(db.Float, default=0.0)
    expected_return_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20))


    def calculate_rent_fee(self):
        
        if self.return_date is None:
        
            return None  # Book hasn't been returned yet
        
        else:

            # Convert expected_return_date to datetime with time component
            expected_return_datetime = datetime.combine(self.expected_return_date, datetime.min.time())

            expected_return_date = expected_return_datetime.date()

            days_overdue = (self.return_date.date() - expected_return_date).days
            rent_fee = max(0, days_overdue * 10)  # Adjust the penalty calculation as needed

            if rent_fee >= 500:

                rent_fee = 500
            
            return rent_fee