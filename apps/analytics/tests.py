from django.test import TestCase

from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.users.models import CustomUser
from apps.transactions.models import Transaction

# Create your tests here.

class AnalyticsTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.admin = CustomUser.objects.create_user(
            username='adminuser',
            password='pass123',
            role='admin'
        )
        self.viewer = CustomUser.objects.create_user(
            username='vieweruser',
            password='pass123',
            role='viewer'
        )

        Transaction.objects.create(
            user=self.admin,
            amount=50000,
            transaction_type='income',
            date='2025-01-10'
        )
        Transaction.objects.create(
            user=self.admin,
            amount=1500,
            transaction_type='expense',
            date='2025-01-15'
        )

        self.summary_url = reverse('summary')

    def _get_token(self, username, password):
        response = self.client.post(
            reverse('login'),
            {'username': username, 'password': password},
            format='json'
        )
        return response.data['access']

    def test_admin_can_access_summary(self):
        token = self._get_token('adminuser', 'pass123')
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        response = self.client.get(self.summary_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_income', response.data)
        self.assertIn('balance', response.data)

    def test_viewer_blocked_from_summary(self):
        token = self._get_token('vieweruser', 'pass123')
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        response = self.client.get(self.summary_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_summary_correct_calculations(self):
        token = self._get_token('adminuser', 'pass123')
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        response = self.client.get(self.summary_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['total_income']), 50000.0)
        self.assertEqual(float(response.data['total_expenses']),1500.0)
        self.assertEqual(float(response.data['balance']),48500.0)

