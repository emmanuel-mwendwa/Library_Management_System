import unittest
import json
import base64

from flask import url_for

from tests import BaseTestConfig

from app.models import Book

from datetime import datetime


class BookTestCase(BaseTestConfig):

    user_details = {
    "username": "johndoe@gmail.com",
    "password": "password123"
    }
   

    def test_create_book(self):

        with self.client:

            headers = {
                "Authentication": f"Basic {base64.b64encode('{userdetails.username}:{userdetails.password}'.encode('utf-8')).decode('utf-8')}",
                "Content-Type": "application/json"
            }
            
            book = {
                'title': 'Test Book',
                'author': 'John Doe',
                'publication_date': '2020-01-01',
                'isbn': '123-4567890123',
                'available_copies': 5,
                'total_copies': 5
            }

            response = self.client.post('/api/v1/books', headers=headers, data=json.dumps(book))

            self.assertEqual(response.status_code, 201)
            self.assertIn('Book created successfully', str(response.data))


    def test_get_all_books(self):

        self.create_sample_book()

        with self.client:

            response = self.client.get('/api/v1/books')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(len(response.get_json()) > 0)


    def test_get_book(self):

        book = self.create_sample_book()

        with self.client:

            response = self.client.get(f'/api/v1/books/{book.id}')
            self.assertEqual(response.status_code, 200)
            self.assertIn('Sample Book', response.get_data(as_text=True))


    def test_update_book(self):

        book = self.create_sample_book()

        with self.client:

            response = self.client.put(f'/api/v1/books/{book.id}', json={
                'title': 'Updated Book',
                'author': 'Updated Author'
            })

            self.assertEqual(response.status_code, 200)
            self.assertIn('Book updated successfully', response.get_data(as_text=True))


    def test_delete_book(self):

        book = self.create_sample_book()

        with self.client:

            response = self.client.delete(f'/api/v1/books/{book.id}')
            self.assertEqual(response.status_code, 200)
            self.assertIn('Book deleted successfully', response.get_data(as_text=True))
