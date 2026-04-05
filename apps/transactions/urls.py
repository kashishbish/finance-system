from django.urls import path
from .views import (
    TransactionListCreateView,
    TransactionDetailView,
    CategoryListCreateView,
)

urlpatterns = [
    path('', TransactionListCreateView.as_view(), name='transaction-list'),
    path('<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
]