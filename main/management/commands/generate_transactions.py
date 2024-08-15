import random
from faker import Faker
from django.core.management.base import BaseCommand
from main.models import Transaction, Category, User

class Command(BaseCommand):
    help = "Generate random transactions for testing purposes"

    def handle(self, *args, **kwargs):
        fake = Faker()

        #create categories
        categories = [
            'Bills', 
            'Food', 
            'Entertainment', 
            'Clothes', 
            'Rent', 
            'Housing', 
            'Salary', 
            'Transportation', 
            'Medical', 
            'Other'
            ]

        for category in categories:
            Category.objects.get_or_create(category_name=category)

        #get the user
        user = User.objects.filter(username='admin').first()
        if not user:
            user = User.objects.create_superuser(username='admin', password='password')

        #create transactions
        categories = Category.objects.all()
        types = [x[0] for x in Transaction.TRANSACTION_TYPE_CHOICES]
        for i in range(20):
            Transaction.objects.create(
                transaction_user = user,
                transaction_category = random.choice(categories),
                transaction_type = random.choice(types),
                transaction_amount = random.uniform(0, 2500),
                transaction_date = fake.date_between(start_date='-1y', end_date='today'),
            )