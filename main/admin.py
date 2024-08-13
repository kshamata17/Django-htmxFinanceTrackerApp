from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)

@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_user', 'transaction_category', 'transaction_type', 'transaction_amount', 'transaction_date')