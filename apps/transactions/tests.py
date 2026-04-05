from django.test import TestCase

from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from apps.users.models import CustomUser
from .models import Transaction, Category


# Create your tests here.
class TransactionTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = CustomUser.objects.create_user(
            username='transuser',
            password='pass123',
            role='admin'
        )

        self.category = Category.objects.create(name='Food')

        login_response = self.client.post(
            reverse('login'),
            {'username': 'transuser', 'password': 'pass123'},
            format='json'
        )
        token = login_response.data['access']
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )

        self.list_url   = reverse('transaction-list')

    def test_create_transaction_success(self):
        data = {
            'amount':           '1500.00',
            'transaction_type': 'expense',
            'category':         self.category.id,
            'date':             '2025-01-15',
            'notes':            'Test transaction'
        }
        response = self.client.post(
            self.list_url, data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Transaction.objects.filter(user=self.user).count(), 1
        )

    def test_create_transaction_negative_amount(self):
        data = {
            'amount':           '-500',
            'transaction_type': 'expense',
            'date':             '2025-01-15',
        }
        response = self.client.post(
            self.list_url, data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_transaction_future_date(self):
        
        data = {
            'amount':           '500',
            'transaction_type': 'expense',
            'date':             '2099-01-01',
        }
        response = self.client.post(
            self.list_url, data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_list_transactions(self):
        
        Transaction.objects.create(
            user=self.user,
            amount=1000,
            transaction_type='income',
            date='2025-01-15'
        )
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_filter_by_type(self):
        
        Transaction.objects.create(
            user=self.user, amount=1000,
            transaction_type='income', date='2025-01-15'
        )
        Transaction.objects.create(
            user=self.user, amount=500,
            transaction_type='expense', date='2025-01-15'
        )
        response = self.client.get(f'{self.list_url}?type=income')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_unauthenticated_request_blocked(self):
        """Request without token returns 401."""
        self.client.credentials()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)