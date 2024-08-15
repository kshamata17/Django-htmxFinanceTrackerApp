from datetime import datetime
import factory
from main.models import Category, Transaction, User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ["username",]

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Sequence(lambda n: f"user{n}")

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ["category_name",]

    category_name = factory.Iterator(
        ["Food", "Entertainment", "Shopping", "Rent"]
    )

class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction
        
    transaction_user = factory.SubFactory(UserFactory)
    transaction_category = factory.SubFactory(CategoryFactory)
    transaction_amount = 5
    transaction_date = factory.Faker(
        "date_between",
        start_date = datetime(year=2021, month=1, day=1).date(),
        end_date = datetime.now().date(),
    )
    transaction_type = factory.Iterator(
        [
            x[0] for x in Transaction.TRANSACTION_TYPE_CHOICES
        ]
    )
