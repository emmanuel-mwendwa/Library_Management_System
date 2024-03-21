import unittest
from app import create_app, db

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
        