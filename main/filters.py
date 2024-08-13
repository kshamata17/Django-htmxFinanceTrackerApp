import django_filters
from .models import Transaction

class TransactionFilter(django_filters.FilterSet):
    transaction_filter_type = django_filters.ChoiceFilter(
        choices=Transaction.TRANSACTION_TYPE_CHOICES,
        field_name = 'transaction_type',
        lookup_expr = 'iexact',
        empty_label = 'Any',
        )

    class Meta:
        model = Transaction
        fields = ('transaction_type',)