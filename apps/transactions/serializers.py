from rest_framework import serializers
from .models import Transaction, Category


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['id', 'name']


class TransactionSerializer(serializers.ModelSerializer):
    

    # For READ — shows full category object in response
    category_name = serializers.SerializerMethodField()

    # For READ — shows username
    user_username = serializers.CharField(
        source='user.username',
        read_only=True
    )

    class Meta:
        model = Transaction
        fields = [
            'id',
            'user_username',
            'amount',
            'transaction_type',
            'category',        # write field — send category ID when creating
            'category_name',   # read field  — see category name in response
            'date',
            'notes',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'user_username', 'category_name']

    def get_category_name(self, obj):
        
        if obj.category:
            return obj.category.name
        return None

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Amount must be greater than zero."
            )
        return value

    def validate_date(self, value):
        from datetime import date
        if value > date.today():
            raise serializers.ValidationError(
                "Transaction date cannot be in the future."
            )
        return value