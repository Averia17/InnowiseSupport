from decouple import config
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class BaseTestCase(APITestCase):

    def setUp(self):
        self.email = config('TEST_EMAIL')
        self.username = config('TEST_USERNAME')
        self.password = config('PASSWORD')
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

    def test_verification(self):
        response = self.client.post('/api/token-verify/', {'token': 'abc'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorization(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='JWT ' + 'abc')
        response = self.client.get('/api/tickets/', data={'format': 'json'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TicketViewSetTestCase(BaseTestCase):
    def test_post_ticket(self):
        self.client.login(username=self.username, password=self.password)

        response = self.client.post("/api/tickets/", {'title': 'lags'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_tickets(self):
        self.client.login(username=self.username, password=self.password)

        response = self.client.get("/api/tickets/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_first_ticket(self):
        self.client.login(username=self.username, password=self.password)
        self.client.post("/api/tickets/", {'title': 'lags'})
        response = self.client.get("/api/tickets/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
