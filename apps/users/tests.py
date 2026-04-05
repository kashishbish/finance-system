from django.test import TestCase

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import CustomUser

# Create your tests here.

class UserAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url    = reverse('login')

    def test_register_success(self):
        data = {
            'username': 'testuser',
            'password': 'testpass123',
            'email':    'test@example.com',
            'role':     'viewer'
        }

        response = self.client.post(
            self.register_url,
            data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertTrue(
            CustomUser.objects.filter(username='testuser').exists()
        )

    def test_register_duplicate_username(self):
        CustomUser.objects.create_user(
            username='existinguser',
            password='pass123'
        )

        data = {
            'username': 'existinguser',
            'password': 'newpass123'
        }

        response = self.client.post(
            self.register_url,
            data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
    
    def test_login_success(self):

        CustomUser.objects.create_user(
            username='loginuser',
            password='correctpass'
        )
        data = {'username': 'loginuser', 'password': 'correctpass'}
        response = self.client.post(
            self.login_url, data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_wrong_password(self):
        """Wrong password returns 401 and no token."""
        CustomUser.objects.create_user(
            username='myuser',
            password='correctpass'
        )
        data = {'username': 'myuser', 'password': 'wrongpass'}
        response = self.client.post(
            self.login_url, data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', response.data)