import plotly.express as px
from django.db.models import Sum

from .models import Category

def plot_income_expenses_bar_chart(qs):
    x_vals = ['Income', 'Expenditure']

    #sum of income and expenses
    total_income = qs.filter(transaction_type='income').aggregate(
        total = Sum('transaction_amount')
        )['total'] or 0

    total_expenses = qs.filter(transaction_type='expense').aggregate(
        total = Sum('transaction_amount')
        )['total'] or 0
    
    fig = px.bar(x=x_vals, y=[total_income, total_expenses], color=x_vals)
    return fig

def plot_category_pie_chart(qs):
    count_per_category = (
        qs.order_by('transaction_category').values('transaction_category')
        .annotate(total=Sum('transaction_amount')
        )
    )
    category_pks = count_per_category.values_list('transaction_category', flat=True).order_by('transaction_category').distinct()
    category_names = Category.objects.filter(pk__in=category_pks).order_by('pk').values_list('category_name', flat=True)
    total_amounts = count_per_category.values_list('total', flat=True)

    fig = px.pie(values=total_amounts, names=category_names)
    fig.update_layout(title_text='Total amount per category')
    return fig