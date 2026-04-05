from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from apps.transactions.models import Transaction
from apps.transactions.serializers import TransactionSerializer

# Create your views here.
class SummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == 'viewer':
            return Response(
                {'error': 'Viewers cannot access analytics'},
                status=status.HTTP_403_FORBIDDEN
            )
        base_qs = Transaction.objects.filter(
            user=request.user,
            is_deleted=False
        )

        total_income = base_qs.filter(
            transaction_type='income'
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0

        total_expenses = base_qs.filter(
            transaction_type='expense'
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0

        balance           = total_income - total_expenses
        total_transactions = base_qs.count()
        income_count      = base_qs.filter(transaction_type='income').count()
        expense_count     = base_qs.filter(transaction_type='expense').count()

        return Response({
            'total_income':       total_income,
            'total_expenses':     total_expenses,
            'balance':            balance,
            'total_transactions': total_transactions,
            'income_count':       income_count,
            'expense_count':      expense_count,
        }, status=status.HTTP_200_OK)
    
class CategoryBreakdownView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == 'viewer':
            return Response(
                {'error': 'Viewers cannot access analytics'},
                status=status.HTTP_403_FORBIDDEN
            )

        breakdown = Transaction.objects.filter(
            user=request.user,
            is_deleted=False
        ).values(
            'category__name',
            'transaction_type'
        ).annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('category__name')

        return Response({
            'breakdown': list(breakdown)
        }, status=status.HTTP_200_OK)
    
class MonthlyTotalsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == 'viewer':
            return Response(
                {'error': 'Viewers cannot access analytics'},
                status=status.HTTP_403_FORBIDDEN
            )

        monthly = Transaction.objects.filter(
            user=request.user,
            is_deleted=False
        ).annotate(
            month=TruncMonth('date')
        ).values(
            'month',
            'transaction_type'
        ).annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('month')

        formatted = {}
        for entry in monthly:
            month_key = entry['month'].strftime('%Y-%m')
            if month_key not in formatted:
                formatted[month_key] = {
                    'month':   month_key,
                    'income':  0,
                    'expense': 0,
                    'balance': 0
                }
            if entry['transaction_type'] == 'income':
                formatted[month_key]['income']  = float(entry['total'])
            else:
                formatted[month_key]['expense'] = float(entry['total'])

        for month_key in formatted:
            formatted[month_key]['balance'] = (
                formatted[month_key]['income'] -
                formatted[month_key]['expense']
            )

        return Response({
            'monthly_totals': list(formatted.values())
        }, status=status.HTTP_200_OK)


class RecentTransactionsView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        recent = Transaction.objects.filter(
            user=request.user,
            is_deleted=False
        ).select_related('category').order_by('-created_at')[:5]

        serializer = TransactionSerializer(recent, many=True)
        return Response({
            'recent_transactions': serializer.data
        }, status=status.HTTP_200_OK)


