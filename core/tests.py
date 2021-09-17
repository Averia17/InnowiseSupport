from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class BaseTestCase(APITestCase):

    def setUp(self):
        self.email = 'artyom@example.com'
        self.username = 'artyom'
        self.password = 'randomPassword123'
        self.user = User.objects.create_user(
            self.username, self.email, self.password)
        self.data = {
            'username': self.username,
            'password': self.password
        }


class UserTestCase(BaseTestCase):
    def test_registration(self):
        data = {
            'username': 'admin',
            'password': 'randomPasswrod123'
        }
        response = self.client.post("/api/auth/users/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_authentication(self):
        response = self.client.post("/api/login/", self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)
        self.access = response.data['access']
        self.refresh = response.data['refresh']

    def test_verification(self):
        self.test_authentication()
        response = self.client.post('/api/token-verify/', {'token': 'abc'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.post('/api/token-verify/', {'token': self.access}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authorization(self):
        self.test_authentication()

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + 'abc')
        response = client.get('/api/tickets/', data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access)
        response = client.get('/api/tickets/', data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TicketViewSetTestCase(UserTestCase):
    def test_post_ticket(self):
        self.test_authentication()
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access)
        response = client.post("/api/tickets/", {'title': 'lags'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
