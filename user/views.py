from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm

# Create your views here.
def userRegister(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            # messages.success(request, 'You have successfully registered')
            messages.success(request, f'Account created for {username}!')
            return redirect('home')
    
    form = UserRegisterForm()

    context = {
        'form': form,
        'title': 'Register'
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
        'form': form,
        'title': 'Login'
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


@login_required
def userProfileUpdate(request):
    profile = Profile.objects.filter(user=request.user).first()
    
    if profile is None:
        messages.success(request, 'Profile not found. Please create your profile')
        return redirect('user-profile-update')
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully updated your profile')
            return redirect('user-profile')
    
    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form,
        'title': 'Update Profile'
    }

    return render(request, 'user/user-profile-update.html', context)