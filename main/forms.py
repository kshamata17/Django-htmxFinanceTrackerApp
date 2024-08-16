from django import forms
from .models import Transaction, Category

class TransactionForm(forms.ModelForm):
    transaction_category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.RadioSelect()
    )

    class Meta:
        model = Transaction
        fields = ('transaction_category', 'transaction_type', 'transaction_amount', 'transaction_date')
        widgets = {
            'transaction_date': forms.DateInput(attrs={'type': 'date'}),
        }