import pytest
from main.factories import *

@pytest.fixture
def transactions():
    return TransactionFactory.create_batch(20)

@pytest.fixture
def user_transactions():
    user = UserFactory()
    return TransactionFactory.create_batch(20, transaction_user=user)