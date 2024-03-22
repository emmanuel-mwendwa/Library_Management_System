from tests import BaseTestConfig

from app.models import Member, Book, Transaction

import json

import base64


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
