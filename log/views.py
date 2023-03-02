from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CreateUserForm
from .models import *


# Create your views here.


def user_register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Rejestracja przebiegła pomyślnie.')
            return redirect('login')

    context = {'form': form}
    return render(request, 'register.html', context)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        if username == "" or password == "":
            messages.error(request, 'Proszę wypełnić obydwa pola.')
            return redirect('login')

        if User.objects.filter(username=username).exists():
            user = authenticate(request, username=username, password=password)
        else:
            messages.error(request, 'Użytkownik nie istenieje.')
            return redirect('login')

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Nazwa albo hasło są nieprawidłowe.')
            return redirect('login')

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')


def handling_404(request, exception):
    return render(request, '404.html', {})


@login_required(login_url='login')
def home(request):

    nav = request.user.homenavimage
    context = {'image': nav}

    return render(request, 'home.html', context)
