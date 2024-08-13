from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='main-home'),
    path('transactions/', views.transactions, name='main-transactions'),
]