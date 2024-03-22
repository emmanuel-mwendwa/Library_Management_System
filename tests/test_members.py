from tests import BaseTestConfig

from app.models import Member

import json

import base64


class MemberTestCase(BaseTestConfig):


    def test_create_member(self):

        user = self.create_user()        

        with self.client:

            headers = {
                "Authorization": f"Basic {base64.b64encode(f'{user.email}:password123'.encode('utf-8')).decode('utf-8')}",
                "Content-Type": "application/json"
            }

            member = {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com'
            }

            response = self.client.post('/api/v1/members', json=member, headers=headers)
            response_data = response.get_json()

            self.assertEqual(response.status_code, 201)
            self.assertEqual('Member created successfully', str(response_data['message']))

    def test_get_members(self):

        test_member = self.create_test_member()
        user = self.create_user()

        with self.client:

            headers = {
                "Authorization": f"Basic {base64.b64encode(f'{user.email}:password123'.encode('utf-8')).decode('utf-8')}",
                "Content-Type": "application/json"
            }

            response = self.client.get('/api/v1/members', headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(len(response.get_json()) > 0)

    def test_get_member(self):

        test_member = self.create_test_member()
        user = self.create_user()

        with self.client:

            headers = {
                "Authorization": f"Basic {base64.b64encode(f'{user.email}:password123'.encode('utf-8')).decode('utf-8')}",
                "Content-Type": "application/json"
            }

            response = self.client.get(f'/api/v1/members/{test_member.id}', headers=headers)
            self.assertEqual(response.status_code, 200)
            data = response.get_json()

            self.assertEqual(data['first_name'], 'John')
            self.assertEqual(data['last_name'], 'Doe')
            self.assertEqual(data['email'], 'john@example.com')
        

    def test_update_member(self):
        
        test_member = self.create_test_member()
        user = self.create_user()

        with self.client:

            headers = {
                "Authorization": f"Basic {base64.b64encode(f'{user.email}:password123'.encode('utf-8')).decode('utf-8')}",
                "Content-Type": "application/json"
            }

            data = {'first_name': 'UpdatedName'}
            response = self.client.put(f'/api/v1/members/{test_member.id}', json=data, headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['message'], 'Member updated successfully')

            response = self.client.get('/api/v1/members/1', headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['first_name'], 'UpdatedName')


    def test_delete_member(self):
        
        test_member = self.create_test_member()
        user = self.create_user()

        with self.client:

            headers = {
                "Authorization": f"Basic {base64.b64encode(f'{user.email}:password123'.encode('utf-8')).decode('utf-8')}",
                "Content-Type": "application/json"
            }

            response = self.client.delete(f'/api/v1/members/{test_member.id}', headers=headers)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['message'], 'Member deleted successfully')

            response = self.client.get(f'/api/v1/members/{test_member.id}', headers=headers)
            self.assertEqual(response.status_code, 404)