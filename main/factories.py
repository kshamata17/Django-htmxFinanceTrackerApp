from datetime import datetime
import factory
from main.models import Category, Transaction, User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ["username",]

    username = factory.Sequence(lambda n: f"user{n}")
    password = "password"
    email = factory.Sequence(lambda n: f"user{n}@example.com")

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
    transaction_amount = factory.Faker("pydecimal", left_digits=2, right_digits=2, positive=True)
    transaction_date = factory.Faker(
        "date_time",
        start_date = datetime(2020, 1, 1).date(),
        end_date = datetime.now().date(),
    )
    transaction_type = factory.Iterator(
        [x[0] for x in Transaction.TRANSACTION_TYPE_CHOICES]
    )
