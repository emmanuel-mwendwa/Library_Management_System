from faker import Faker

from random import randint

from datetime import datetime, timedelta

from . import db

from .models import Book, Member, Transaction

fake = Faker()
def generate_books(num_books):
    for _ in range(num_books):
        book = Book(
            title=fake.sentence(nb_words=4),
            author=fake.name(),
            publication_date=fake.date_between(start_date='-50y', end_date=datetime.now()),
            isbn=fake.isbn13(),
            total_copies=randint(1, 10)
        )
        db.session.add(book)

def generate_members(num_members):
    for _ in range(num_members):
        member = Member(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
        )
        db.session.add(member)

def generate_transactions(num_transactions):
    for _ in range(num_transactions):
        transaction = Transaction(
            book_id=randint(1, Book.query.count()),
            member_id=randint(1, Member.query.count()),
            issue_date=fake.date_time_between(start_date='-5y', end_date=datetime.now()),
            return_date=fake.date_time_between(start_date='-5y', end_date=datetime.now()),
            expected_return_date=fake.date_time_between(start_date=datetime.now(), end_date=datetime.now()),
            status=fake.random_element(elements=('Borrowed', 'Returned'))
        )
        db.session.add(transaction)

def populate_database(num_books=20, num_members=10, num_transactions=50):
    generate_books(num_books)
    generate_members(num_members)
    # generate_transactions(num_transactions)
    db.session.commit()

if __name__ == "__main__":
    populate_database()
