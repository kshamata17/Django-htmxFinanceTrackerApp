from django import forms
from .models import Transaction, Category
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your email', 
            'class': 'form-control'
        })
    )

    username = forms.CharField(
        required=True, 
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your username', 
            'class': 'form-control'
        })
    )

    password1 = forms.CharField(
        required=True, 
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password', 
            'class': 'form-control'
        })
    )

    password2 = forms.CharField(
        required=True, 
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm your password', 
            'class': 'form-control'
        })
    )
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

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

    