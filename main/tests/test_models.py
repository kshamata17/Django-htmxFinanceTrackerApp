import pytest
from main.models import Transaction, Category


@pytest.mark.django_db
def test_queryset_get_income_method(transactions):
    qs = Transaction.objects.get_income()
    assert qs.count() > 0
    assert all(
        [transaction.transaction_type == 'income' for transaction in qs]
    )

@pytest.mark.django_db
def test_queryset_get_expense_method(transactions):
    qs = Transaction.objects.get_expense()
    assert qs.count() > 0
    assert all(
        [transaction.transaction_type == 'expense' for transaction in qs]
    )
