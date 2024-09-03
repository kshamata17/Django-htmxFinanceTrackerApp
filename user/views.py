from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile

# Create your views here.
def userRegister(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'You have successfully registered')
            return redirect('home')
    
    form = UserRegisterForm()

    context = {
        'form': form
    }

    return render(request, 'user/register.html', context)

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
                return redirect('main-home')
    
    form = UserLoginForm()

    context = {
        'form': form
    }
    return render(request, 'user/login.html', context)

@login_required
def userProfile(request):
    profile = Profile.objects.filter(user=request.user).first()

    context = {
        'profile': profile,
        'title': 'Profile'
    }
    return render(request, 'user/user-profile.html', context)