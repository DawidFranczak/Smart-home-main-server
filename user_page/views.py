from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from django.contrib import messages
from .forms import ChangePasswordForm, ChangeEmailForm, ChangeImageForm

# Create your views here.


@login_required(login_url='login')
def user_page(request):
    return render(request, 'user_page.html')


@login_required(login_url='login')
def user_change_password(request):

    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            username = request.user
            password = request.POST.get('new_password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, 'Zmiana hasła przebiegła pomyślnie')
            return redirect('user_page')

    form = ChangePasswordForm(request.user)
    context = {'action': 'password',
               'form': form}

    return render(request, 'user_page.html', context)


@login_required(login_url='login')
def user_change_email(request):

    if request.method == 'POST':
        form = ChangeEmailForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Zmiana emaila przebiegła pomyślnie')
            return redirect('user_page')

    form = ChangeEmailForm(request.user)
    old = request.user.email
    context = {'action': 'email',
               'form': form,
               'old': old}

    return render(request, 'user_page.html', context)


@login_required(login_url='login')
def user_change_image(request):
    form = ChangeImageForm(request.user)

    if request.method == 'POST':
        form = ChangeImageForm(request.user, request.POST, request.FILES)

        if request.POST.get('save') is not None:

            if form.is_valid():
                form.save(request.user)
                messages.success(request, 'Udało się zmienić zdjęcie(a)')
                return redirect('user_page')
        else:
            form.reset(request.user)
            messages.success(request, 'Zresetowano zdjęcia')
            return redirect('user_page')

    context = {'action': 'image',
               'form': form}

    return render(request, 'user_page.html', context)


@login_required(login_url='login')
def user_delete(request):
    if request.method == 'POST':

        request.user.delete()
        messages.success(request, 'Konto zostało usunięte')
        return redirect('login')

    context = {'action': 'delete'}

    return render(request, 'user_page.html', context)
