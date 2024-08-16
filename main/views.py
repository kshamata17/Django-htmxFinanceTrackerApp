from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Transaction
from .filters import TransactionFilter
from .forms import TransactionForm

# Create your views here.
def home(request):
    user = request.user
    context = {'user': user}
    return render(request, 'main/home.html', context)

@login_required
def transactions_list(request):
    transaction_filter = TransactionFilter(
        request.GET, 
        queryset=Transaction.objects.filter(transaction_user=request.user).select_related('transaction_category')
    )
    total_income = transaction_filter.qs.get_total_incomes()
    total_expense = transaction_filter.qs.get_total_expenses()
    
    context = {
        'filter': transaction_filter,
        'total_income': total_income,
        'total_expense': total_expense,
        'net_income': total_income - total_expense
    }

    if request.htmx:
        return render(request, 'main/partials/transactions-container.html', context)
    
    return render(request, 'main/transactions.html', context)

@login_required
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.transaction_user = request.user
            transaction.save()
            context = {'message': 'Transaction created successfully!'}
            return render(request, 'main/partials/transaction-success.html', context)
    context = {
        'form': TransactionForm()
        }
    return render(request, 'main/partials/create-transaction.html', context)
