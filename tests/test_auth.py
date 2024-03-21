import unittest

from app import db

from app.models import User

from tests import BaseTestConfig

class AuthTestCase(BaseTestConfig):

    def create_user(self, email='john@example.com', password='password123'):
        
        user = User(first_name='John', last_name='Doe', email=email, password=password)
        
        db.session.add(user)
        db.session.commit()
        
        return user

    def test_register_user(self):

        response = self.client.post('/api/v1/register', json={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password': 'password123'
        })

        self.assertEqual(response.status_code, 201)

        data = response.get_json()

        self.assertEqual(data['message'], 'User registered successfully.')


    def test_login(self):

        # Create a user to login
        self.create_user()

        # Test user login
        response = self.client.post('api/v1/login', json={
            'email': 'john@example.com',
            'password': 'password123'
        })

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'Logged in successfully.')


    def test_logout(self):

        # Create a user to login
        user = self.create_user()

        # Login the user
        self.client.post('/api/v1/login', json={
            'email': 'john@example.com',
            'password': 'password123'
        })

        # Test user logout
        response = self.client.get('/api/v1/logout')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'You have been logged out.')