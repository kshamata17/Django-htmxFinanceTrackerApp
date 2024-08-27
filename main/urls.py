from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='main-home'),
    path('transactions/', views.transactions_list, name='main-transactions'),
    path('transactions/create', views.create_transaction, name='create-transaction'),
    path('transactions/login', views.user_login, name='login'),
    path('transactions/register', views.user_register, name='register'),

    path('transactions/<int:pk>/update', views.update_transaction, name='update-transaction'),
    path('transactions/<int:pk>/delete', views.delete_transaction, name='delete-transaction'),

    path('get-transactions/', views.get_transactions, name='get-transactions'),
]