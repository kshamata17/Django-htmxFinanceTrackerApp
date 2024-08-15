import pytest
from main.models import Transaction, Category


@pytest.mark.django_db
def test_queryset_get_income_method(transactions):
    qs = Transaction.objects.get_incomes()
    assert qs.count() > 0
    assert all(
        [transaction.transaction_type == 'income' for transaction in qs]
    )

@pytest.mark.django_db
def test_queryset_get_expense_method(transactions):
    qs = Transaction.objects.get_expenses()
    assert qs.count() > 0
    assert all(
        [transaction.transaction_type == 'expense' for transaction in qs]
    )
@pytest.mark.django_db
def test_queryset_get_total_income_method(transactions):
    total_income = Transaction.objects.get_total_incomes()
    assert total_income == sum(t.transaction_amount for t in transactions if t.transaction_type == 'income')

@pytest.mark.django_db
def test_queryset_get_total_expenses_method(transactions):
    total_expenses = Transaction.objects.get_total_expenses()
    assert total_expenses == sum(t.transaction_amount for t in transactions if t.transaction_type == 'expense')