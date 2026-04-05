from django.urls import path
from .views import (
    SummaryView,
    CategoryBreakdownView,
    MonthlyTotalsView,
    RecentTransactionsView,
)

urlpatterns = [
    path('summary/',SummaryView.as_view(),name='summary'),
    path('category-breakdown/', CategoryBreakdownView.as_view(),name='category-breakdown'),
    path('monthly/',MonthlyTotalsView.as_view(),name='monthly-totals'),
    path('recent/',RecentTransactionsView.as_view(),name='recent'),
]