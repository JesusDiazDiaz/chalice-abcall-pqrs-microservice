import unittest
from unittest.mock import patch, MagicMock
import boto3
from chalice.test import Client
from moto import mock_aws
import app


class TestClientService(unittest.TestCase):

    @mock_aws
    def setUp(self):
        self.cognito_client = boto3.client('cognito-idp', region_name='us-east-1')
        self.user_pool_id = self.cognito_client.create_user_pool(PoolName='TestPool')['UserPool']['Id']
        self.client_id = self.cognito_client.create_user_pool_client(
            UserPoolId=self.user_pool_id,
            ClientName='TestClient'
        )['UserPoolClient']['ClientId']

        self.test_client = Client(app.app)

    def tearDown(self):
        self.cognito_client = None
        self.test_client = None

    @patch('app.cognito_client', autospec=True)
    def test_get_clients(self, mock_cognito):
        mock_cognito.list_users.return_value = {
            'Users': [
                {
                    'Username': 'testuser',
                    'Attributes': [
                        {'Name': 'email', 'Value': 'testuser@example.com'},
                        {'Name': 'custom:user_role', 'Value': 'superadmin'}
                    ]
                }
            ]
        }

        response = self.test_client.http.get('/clients')

        self.assertEqual(response.status_code, 200)
        self.assertIn('testuser', response.json_body)

    @patch('app.cognito_client', autospec=True)
    def test_create_client(self, mock_cognito):
        client_data = {
            "perfil": "Test Perfil",
            "id_type": "cedula",
            "legal_name": "Test Legal Name",
            "id_number": "1234567890",
            "address": "123 Test Street",
            "type_document_rep": "cedula",
            "id_rep_lega": "987654321",
            "name_rep": "John",
            "last_name_rep": "Doe",
            "email_rep": "john.doe@example.com",
            "plan_type": "emprendedor"
        }

        response = self.test_client.http.post('/client', json=client_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json_body['message'], "Client created successfully")

    @patch('app.cognito_client', autospec=True)
    def test_get_client_by_id(self, mock_cognito):
        mock_cognito.admin_get_user.return_value = {
            'Username': 'testuser',
            'UserAttributes': [
                {'Name': 'email', 'Value': 'testuser@example.com'},
                {'Name': 'custom:user_role', 'Value': 'superadmin'}
            ]
        }

        response = self.test_client.http.get('/client/1')

        self.assertEqual(response.status_code, 200)
        self.assertIn('testuser', response.json_body['data']['Username'])

    @patch('app.cognito_client', autospec=True)
    def test_delete_client(self, mock_cognito):
        mock_cognito.admin_delete_user.return_value = {}

        response = self.test_client.http.delete('/client/1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json_body['status'], 'success')


if __name__ == '__main__':
    unittest.main()
