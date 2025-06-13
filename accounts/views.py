from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserRegisterForm
from .models import User  
from django.views.decorators.csrf import csrf_protect

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Check if username already exists
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                messages.error(request, 'Username already taken. Please choose a different one.')
                return render(request, 'accounts/register.html', {'form': form})
            
            # Check if email already exists
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                messages.error(request, 'Email already registered. Please use a different email or login.')
                return render(request, 'accounts/register.html', {'form': form})
            
            # If all checks pass, create user
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now login.')
            return redirect('login')
        else:
            # Form is invalid (password mismatch, etc)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('problems:problem_list')
        else:
            # Check if username exists but password is wrong
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Incorrect password. Please try again.')
            else:
                messages.error(request, 'Account does not exist. Please register first.')
    
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')