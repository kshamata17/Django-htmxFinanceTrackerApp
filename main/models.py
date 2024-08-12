from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('income', 'INCOME'),
        ('expense', 'EXPENSE'),
    )
    transaction_user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateField()

    def __str__(self):
        return f"{self.transaction_type} of {self.transaction_amount} on {self.transaction_date} by {self.transaction_user}"

