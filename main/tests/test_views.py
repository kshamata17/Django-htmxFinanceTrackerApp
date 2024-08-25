import pytest
from django.urls import reverse
from datetime import datetime, timedelta

from main.models import Category, Transaction
from pytest_django.asserts import assertTemplateUsed

@pytest.mark.django_db
def test_total_values_appear_on_list_page(user_transactions, client):
   user = user_transactions[0].transaction_user
   client.force_login(user)

   income_total = sum(t.transaction_amount for t in user_transactions if t.transaction_type == 'income')
   expense_total = sum(t.transaction_amount for t in user_transactions if t.transaction_type == 'expense')
   net = income_total - expense_total

   response = client.get(reverse('main-transactions'))
   assert response.context['total_income'] == income_total
   assert response.context['total_expense'] == expense_total
   assert response.context['net_income'] == net


@pytest.mark.django_db
def test_transaction_type_filters(user_transactions, client):
   user = user_transactions[0].transaction_user
   client.force_login(user)

   # income check
   GET_params = {'transaction_type': 'income'}

   response = client.get(reverse('main-transactions'), GET_params)

   qs = response.context['filter'].qs

   for transaction in qs:
      assert transaction.transaction_type == 'income'

   # expense check
   GET_params = {'transaction_type': 'expense'}

   response = client.get(reverse('main-transactions'), GET_params)

   qs = response.context['filter'].qs

   for transaction in qs:
      assert transaction.transaction_type == 'expense'

@pytest.mark.django_db
def test_start_end_date_filter(user_transactions, client):
    user = user_transactions[0].transaction_user
    client.force_login(user)

    start_date_cutoff = datetime.now().date() - timedelta(days=120)

    GET_params = {'start_date': start_date_cutoff}
    response = client.get(reverse('main-transactions'), GET_params)

    qs = response.context['filter'].qs

    for transaction in qs:
      assert transaction.transaction_date >= start_date_cutoff

    end_date_cutoff = datetime.now().date() - timedelta(days=20)

    GET_params = {'end_date': end_date_cutoff}
    response = client.get(reverse('main-transactions'), GET_params)

    qs = response.context['filter'].qs

    for transaction in qs:
        assert transaction.transaction_date <= end_date_cutoff

@pytest.mark.django_db
def test_category_filter(user_transactions, client):
    user = user_transactions[0].transaction_user
    client.force_login(user)

    # get first two categories' PKs
    category_pks = Category.objects.all()[:2].values_list('pk', flat=True)
    GET_params = {'category': category_pks}

    response = client.get(reverse('main-transactions'), GET_params)

    qs = response.context['filter'].qs

    for transaction in qs:
        assert transaction.transaction_category.pk in category_pks

@pytest.mark.django_db
def test_add_transaction_request(user, transaction_dict_params, client):
   client.force_login(user)
   user_transaction_count = Transaction.objects.filter(transaction_user=user).count()

   # send request with transaction data
   headers = {'HTTP_HX-Request': 'true'}
   response = client.post(
      reverse('create-transaction'), 
      transaction_dict_params, 
      **headers
   )

   assert Transaction.objects.filter(transaction_user=user).count() == user_transaction_count + 1

   assertTemplateUsed(response, 'main/partials/transaction-success.html')