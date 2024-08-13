from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Transaction
from .filters import TransactionFilter

# Create your views here.
def home(request):
    user = request.user
    context = {'user': user}
    return render(request, 'main/home.html', context)

@login_required
def transactions(request):
    transaction_filter = TransactionFilter(
        request.GET, queryset=Transaction.objects.filter(transaction_user=request.user)
     )
    transactions = transaction_filter.qs
    context = {'filter': transaction_filter}
    return render(request, 'main/transactions.html', context)
