from import_export import resources, fields
from .models import Transaction, Category
from import_export.widgets import ForeignKeyWidget

class TransactionResource(resources.ModelResource):
    transaction_category = fields.Field(
        column_name='transaction_category',
        attribute='transaction_category',
        widget=ForeignKeyWidget(Category, 'category_name')
    )
    class Meta:
        model = Transaction
        fields = (
            'transaction_category', 
            'transaction_type', 
            'transaction_amount', 
            'transaction_date',
        )