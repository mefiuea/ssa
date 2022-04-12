from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.urls import reverse_lazy

from users_app.forms import RegistrationForm


def signup_view(request):
    if request.method == 'POST':
        # form = UserCreationForm(request.POST)
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            return redirect(reverse_lazy('home_page_app:home_view'))
    else:
        # form = UserCreationForm()
        form = RegistrationForm()

    return render(request, 'users_app/signup.html', context={'form': form})


def login_view(request):
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
    if request.method == 'POST':
        logout(request)
        return render(request, 'users_app/logged_out.html')
    user = request.user
    return render(request, 'users_app/logout.html', context={'user': user})


# def reset_password_view(request):
#     if request.method == 'POST':
#         form = PasswordResetForm()
#         if form.is_valid():
#             print('walidacja maila poprawna')
#         else:
#             print('walidacja maila niepoprawna!')
#     else:
#         form = PasswordResetForm()
#     return render(request, 'users_app/reset_password.html', context={'form': form})
