import pytest
from main.factories import *

@pytest.fixture
def transactions():
    return TransactionFactory.create_batch(20)

@pytest.fixture
def user_transactions():
    user = UserFactory()
    return TransactionFactory.create_batch(20, transaction_user=user)

@pytest.fixture
def user():
    return UserFactory()

@pytest.fixture
def transaction_dict_params(user):
    transaction = TransactionFactory.create(transaction_user=user)
    return {
        'transaction_date': transaction.transaction_date,
        'transaction_type': transaction.transaction_type,
        'transaction_category': transaction.transaction_category,
        'transaction_amount': transaction.transaction_amount
    }