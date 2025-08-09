from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomSignupForm

# Signup View
# Handles user registration with validation and user-friendly feedback
def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'🎉 Welcome {user.username}! Your account was created successfully. You are now logged in.')
            return redirect('profile')
        else:
            # Show a friendly error message if form is not valid
            messages.error(request, 'Oops! Please check the highlighted fields and try again.')
    else:
        form = CustomSignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

# Login View
# Authenticates user and provides helpful error messages
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'👋 Welcome back, {user.username}!')
            return redirect('profile')
        else:
            # Show a friendly error message if credentials are wrong
            messages.error(request, 'Sorry, that username and password did not match. Please try again.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

# Logout View
# Logs out user and redirects to login page
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out. See you again soon!')
    return render(request, 'accounts/logout.html')

# Profile View
# Shows a friendly profile page for logged-in users
def profile_view(request):
    if not request.user.is_authenticated:
        messages.info(request, 'Please log in to view your profile.')
        return redirect('login')
    return render(request, 'accounts/profile.html', {'user': request.user})
