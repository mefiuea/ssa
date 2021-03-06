from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy

from users_app.forms import RegistrationForm
from management_app.models import Profile


def signup_view(request):
    """Function to display registration form. It allows to signup user to database.
    This function also creat empty profile for specific user."""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            # create empty profile for current user
            Profile.objects.create(owner=user)
            return redirect(reverse_lazy('users_app:login_view'))
    else:
        form = RegistrationForm()

    return render(request, 'users_app/signup.html', context={'form': form})


def login_view(request):
    """Function to display login form. It allows authenticating user."""
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse_lazy('home_page_app:home_view'))
    else:
        form = AuthenticationForm()

    return render(request, 'users_app/login.html', context={'form': form})


def logout_view(request):
    """Function to display logout form. It allows deleting session for current user."""
    if request.method == 'POST':
        logout(request)
        return render(request, 'users_app/logged_out.html')
    user = request.user
    return render(request, 'users_app/logout.html', context={'user': user})
