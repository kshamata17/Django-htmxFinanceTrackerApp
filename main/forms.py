from django import forms
from .models import Transaction, Category

class TransactionForm(forms.ModelForm):
    transaction_category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.RadioSelect()
    )
    class Meta:
        model = Transaction
        fields = (
            'transaction_category', 
            'transaction_type', 
            'transaction_amount', 
            'transaction_date'
        )
        widgets = {
            'transaction_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_transaction_amount(self):
        transaction_amount = self.cleaned_data['transaction_amount']
        if transaction_amount <= 0:
            raise forms.ValidationError("Amount must be a positive number.")
        return transaction_amount

    