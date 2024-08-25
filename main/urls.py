from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='main-home'),
    path('transactions/', views.transactions_list, name='main-transactions'),
    path('transactions/create', views.create_transaction, name='create-transaction'),
    path('transactions/login', views.login, name='login'),
    path('transactions/register', views.register, name='register'),
]