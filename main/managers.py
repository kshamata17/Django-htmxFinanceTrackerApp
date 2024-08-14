from django.db import models

class TransactionQuerySet(models.QuerySet):
    def get_expenses(self):
        return self.filter(transaction_type = 'expense')

    def get_incomes(self):
        return self.filter(transaction_type = 'income')
    
    def get_total_expenses(self):
        return self.get_expenses().aggregate(
            total=models.Sum('transaction_amount')
        )['total'] or 0

    def get_total_incomes(self):
        return self.get_incomes().aggregate(
            total=models.Sum('transaction_amount')
        )['total'] or 0