from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.
def userLogin(request, *args, **kwargs):
    if request.method == 'POST':
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.success(request, 'You have successfully logged in')
                return redirect('home')
    
    form = UserLoginForm()
    return render(request, 'user/login.html')

def userRegister(request):
    return render(request, 'user/register.html')
