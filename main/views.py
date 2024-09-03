from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.conf import settings
from .resources import TransactionResource
from django.http import HttpResponse

from .models import Transaction
from .filters import TransactionFilter
from .forms import TransactionForm
from django_htmx.http import retarget
from main.charting import plot_income_expenses_bar_chart, plot_category_pie_chart

# Create your views here.
def home(request):
    user = request.user
    context = {
        'user': user,
        'title': 'Home'
        }
    return render(request, 'main/home.html', context)

@login_required
def transactions_list(request):
    transaction_filter = TransactionFilter(
        request.GET, 
        queryset=Transaction.objects.filter(transaction_user=request.user).select_related('transaction_category')
    )
    paginator = Paginator(transaction_filter.qs, settings.PAGE_SIZE)
    transaction_page = paginator.page(1)


    total_income = transaction_filter.qs.get_total_incomes()
    total_expense = transaction_filter.qs.get_total_expenses()
    
    context = {
        'transactions': transaction_page,
        'filter': transaction_filter,
        'total_income': total_income,
        'total_expense': total_expense,
        'net_income': total_income - total_expense,
        'title': 'Transactions'
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
        else:
            context = {'form': form}
            response = render(request, 'main/partials/create-transaction.html', context)
            return retarget(response, '#transaction-block')
    context = {
        'form': TransactionForm()
        }
    return render(request, 'main/partials/create-transaction.html', context)

@login_required
def update_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            transaction = form.save()
            context = {'message': 'Transaction updated successfully!'}
            return render(request, 'main/partials/transaction-success.html', context)
        else:
            context = {
                'form': form,
                'transaction': transaction,
                }  
            response = render(request, 'main/partials/update-transaction.html', context)
            return retarget(response, '#transaction-block')
        
    context = {
        'form': TransactionForm(instance=transaction),
        'transaction': transaction,
        'title': 'Update Transaction',    
        }  
    return render(request, 'main/partials/update-transaction.html', context)

@login_required
@require_http_methods(["DELETE"])
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, transaction_user=request.user)
    transaction.delete()
    context = {
        'message': f"Transaction of {transaction.transaction_amount} on {transaction.transaction_date} deleted successfully!"
        }
    return render(request, 'main/partials/transaction-success.html', context)

@login_required
def get_transactions(request):
    page = request.GET.get('page', 1) 
    transaction_filter = TransactionFilter(
        request.GET, 
        queryset=Transaction.objects.filter(transaction_user=request.user).select_related('transaction_category')
    )
    paginator = Paginator(transaction_filter.qs, settings.PAGE_SIZE)
    context = {
        'transactions': paginator.page(page),
    }
    return render(request, 'main/partials/transactions-container.html#transaction_list', context)

def transaction_charts(request):
    transaction_filter = TransactionFilter(
        request.GET, 
        queryset=Transaction.objects.filter(transaction_user=request.user).select_related('transaction_category')
    )
    income_expense_bar = plot_income_expenses_bar_chart(transaction_filter.qs)
    category_income_pie = plot_category_pie_chart(
        transaction_filter.qs.filter(transaction_type='income')
        )
    category_expense_pie = plot_category_pie_chart(
        transaction_filter.qs.filter(transaction_type='expense')
        )
    context = {
        'filter': transaction_filter,
        'income_expense_barchart': income_expense_bar.to_html(),
        'category_income_piechart': category_income_pie.to_html(),
        'category_expense_piechart': category_expense_pie.to_html(),
        'title': 'Charts'
    }
    if request.htmx:
        return render(request, 'main/partials/charts-container.html', context)
    return render(request, 'main/charts.html', context)

@login_required
def export(request): 
    if request.htmx:
        return HttpResponse(headers={'HX-Redirect': request.get_full_path()}) 
    
    transaction_filter = TransactionFilter(
        request.GET, 
        queryset=Transaction.objects.filter(transaction_user=request.user).select_related('transaction_category')
    )  

    data = TransactionResource().export(transaction_filter.qs)
    response = HttpResponse(data.json, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="transactions.json"'
    return response