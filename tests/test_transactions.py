from tests import BaseTestConfig

from app import db

from app.models import Member, Book, Transaction

import json

import base64

from datetime import datetime, timedelta


class TransactionTestCase(BaseTestConfig):

    def test_issue_book(self):

        member = self.create_test_member()
        book = self.create_sample_book()
        user = self.create_user()

        with self.client:

            headers = {
                "Authorization": f"Basic {base64.b64encode(f'{user.email}:password123'.encode('utf-8')).decode('utf-8')}",
                "Content-Type": "application/json"
            }

            issue = {
                'member_id': member.id,
                'book_id': book.id
            }

            response = self.client.post('/api/v1/issue_book', json=issue, headers=headers)

            self.assertEqual(response.status_code, 201)


    def test_return_book(self):

        member = self.create_test_member()
        book = self.create_sample_book()
        user = self.create_user()

        transaction = Transaction(
            book_id=book.id, 
            member_id=member.id, 
            issue_date=datetime.utcnow(), 
            return_date=None, 
            expected_return_date= datetime.utcnow() + timedelta(days=14),
            status="Borrowed"
        )

        db.session.add(transaction)
        db.session.commit()

        with self.client:

            headers = {
                "Authorization": f"Basic {base64.b64encode(f'{user.email}:password123'.encode('utf-8')).decode('utf-8')}",
                "Content-Type": "application/json"
            }

            self.assertIsNotNone(Transaction.query.filter_by(member_id=member.id, book_id=book.id, return_date=None).first())
            self.assertTrue(book.available_copies > 1)

            response = self.client.post('/api/v1/return_book', json={
                'member_id': member.id,
                'book_id': book.id,
                'return_date': datetime.utcnow()
            }, headers=headers)

            self.assertEqual(response.status_code, 200)

            # After returning the book, check if the transaction and book statuses are updated
            returned_transaction = Transaction.query.filter_by(member_id=member.id, book_id=book.id).first()

            # Transaction should now have a return_date
            self.assertIsNotNone(returned_transaction.return_date)

            # Status should be updated to "Returned"
            self.assertEqual(returned_transaction.status, "Returned")  

            updated_book = Book.query.get(book.id)
            self.assertEqual(updated_book.available_copies, 6)


    def test_view_transactions(self):

        user = self.create_user()

        with self.client:

            headers = {
                "Authorization": f"Basic {base64.b64encode(f'{user.email}:password123'.encode('utf-8')).decode('utf-8')}",
                "Content-Type": "application/json"
            }

            response = self.client.get('/api/v1/view_transactions', headers=headers)

            self.assertEqual(response.status_code, 200)
            data = response.json
            self.assertIn('transactions', data)