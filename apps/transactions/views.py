from django.shortcuts import render
from rest_framework import status
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Transaction, Category
from .serializers import TransactionSerializer, CategorySerializer


class TransactionListCreateView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(
            user=request.user,
            is_deleted=False
        ).select_related('category')

        # Read query parameters safely
        transaction_type = request.query_params.get('type')
        category_id      = request.query_params.get('category')
        date_from        = request.query_params.get('date_from')
        date_to          = request.query_params.get('date_to')
        search           = request.query_params.get('search')

        #apply filters
        if transaction_type:
            transactions = transactions.filter(
                transaction_type=transaction_type)
            
        if category_id:
            transactions = transactions.filter(
                category__id=category_id
            )
         
        if date_from:
            transactions = transactions.filter(
                date__gte=date_from
            )

        if date_to:
            transactions = transactions.filter(
                date__lte=date_to
            )
        
        if search:
            transactions = transactions.filter(
                notes__icontains=search
            )
        
        serializer = TransactionSerializer(transactions, many=True)
        return Response({
            'count':   transactions.count(),
            'results': serializer.data }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class TransactionDetailView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        return get_object_or_404(
            Transaction,
            pk=pk,
            user=user,
            is_deleted=False
        )

    def get(self, request, pk):
        transaction = self.get_object(pk, request.user)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        transaction = self.get_object(pk, request.user)
        serializer = TransactionSerializer(
            transaction,
            data=request.data,
            partial=False
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        transaction = self.get_object(pk, request.user)
        transaction.is_deleted = True
        transaction.save()
        return Response(
            {'message': 'Transaction deleted successfully'},
            status=status.HTTP_200_OK
        )


class CategoryListCreateView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.role != 'admin':
            return Response(
                {'error': 'Only admins can create categories'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )