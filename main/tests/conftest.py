import pytest
from main.factories import *


@pytest.fixture
def transactions():
    return TransactionFactory.create_batch(20)