import django_filters
from .models import Transaction, Category
from django import forms

class TransactionFilter(django_filters.FilterSet):

    transaction_filter_type = django_filters.ChoiceFilter(
        choices=Transaction.TRANSACTION_TYPE_CHOICES,
        field_name = 'transaction_type',
        lookup_expr = 'iexact',
        empty_label = 'Any',
        )
    
    start_date = django_filters.DateFilter(
        field_name = 'transaction_date',
        lookup_expr = 'gte',
        label = 'Date From',
        widget = forms.DateInput(
            attrs = {
                'type': 'date',
            }
        )

    )

    end_date = django_filters.DateFilter(
        field_name = 'transaction_date',
        lookup_expr = 'lte',
        label = 'Date To',
        widget = forms.DateInput(
            attrs = {
                'type': 'date',
            }
        )

    )

    category = django_filters.ModelChoiceFilter(
        queryset = Category.objects.all(),
        widget = forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Transaction
        fields = ('transaction_type', 'start_date', 'end_date', 'category')