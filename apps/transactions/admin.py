from django.contrib import admin
from .models import Category, Transaction
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_type', 'amount', 'category', 'date', 'is_deleted')
    list_filter = ('transaction_type', 'is_deleted', 'category')