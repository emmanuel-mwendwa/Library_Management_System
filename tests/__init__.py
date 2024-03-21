import unittest
from app import create_app, db

from app.models import Book

from datetime import datetime


class BaseTestConfig(unittest.TestCase):

    def setUp(self) -> None:
        
        super().setUp()
    
        self.app = create_app("testing")

        self.app_context = self.app.app_context()

        self.app_context.push()

        db.create_all()

        self.client = self.app.test_client()


    def tearDown(self) -> None:
        
        super().tearDown()

        db.drop_all()

        self.app_context.pop()

        self.app = None

        self.client = None

    def create_sample_book(self):

        book = Book(
            title="Sample Book",
            author="Author",
            publication_date=datetime.strptime("2020-01-01", '%Y-%m-%d'),
            isbn="1234567890123",
            available_copies=5,
            total_copies=5
        )

        db.session.add(book)
        db.session.commit()
        
        return book
        