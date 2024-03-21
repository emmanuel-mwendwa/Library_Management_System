from tests import BaseTestConfig

from app.models import Member

import json


class MemberTestCase(BaseTestConfig):


    def test_create_member(self):

        with self.client:

            member = {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com'
            }

            response = self.client.post('/api/v1/members', json=member)
            response_data = response.get_json()

            self.assertEqual(response.status_code, 201)
            self.assertEqual('Member created successfully', str(response_data['message']))

    def test_get_members(self):

        test_member = self.create_test_member()

        with self.client:

            response = self.client.get('/api/v1/members')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(len(response.get_json()) > 0)

    def test_get_member(self):

        test_member = self.create_test_member()

        with self.client:

            response = self.client.get(f'/api/v1/members/{test_member.id}')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()

            self.assertEqual(data['first_name'], 'John')
            self.assertEqual(data['last_name'], 'Doe')
            self.assertEqual(data['email'], 'john@example.com')
        

    def test_update_member(self):
        
        test_member = self.create_test_member()

        with self.client:

            data = {'first_name': 'UpdatedName'}
            response = self.client.put(f'/api/v1/members/{test_member.id}', json=data)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['message'], 'Member updated successfully')

            response = self.client.get('/api/v1/members/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['first_name'], 'UpdatedName')


    def test_delete_member(self):
        
        test_member = self.create_test_member()

        with self.client:

            response = self.client.delete(f'/api/v1/members/{test_member.id}')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['message'], 'Member deleted successfully')

            response = self.client.get(f'/api/v1/members/{test_member.id}')
            self.assertEqual(response.status_code, 404)