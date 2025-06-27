from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import CustomAuthForm, CustomUserCreationForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomAuthForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        else:
            form.errors.clear()
            form.add_error(
                None, ('Введены неправильное имя пользователя или пароль. '
                       'Повторите попытку.'))
    else:
        form = CustomAuthForm()
    return render(request, 'vpn_auth/login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        # Перенаправляем, если пользователь уже авторизован
        return redirect('home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'vpn_auth/register.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
