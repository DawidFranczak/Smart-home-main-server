from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import update_session_auth_hash

from .forms import ChangePasswordForm, ChangeEmailForm, ChangeImageForm

# Create your views here.


class UserPage(TemplateView):
    template_name = 'user_page.html'


class UserChangePassword(View):
    template_name = 'user_page.html'
    form_class = ChangePasswordForm

    def get(self, request):

        context = {'action': 'password',
                   'form': ChangePasswordForm(request.user)}

        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Zmiana hasła przebiegła pomyślnie')
            return redirect('user_page')

        context = {'action': 'password',
                   'form': form}

        return render(request, self.template_name, context)


class UserChangeEmail(View):
    template_name = 'user_page.html'
    form_class = ChangeEmailForm

    def get(self, request):
        form = self.form_class(request.user)
        old = request.user.email
        context = {'action': 'email',
                   'form': form,
                   'old': old}

        return render(request, self.template_name, context)

    def post(self, request):
        form = ChangeEmailForm(request.user, request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Zmiana emaila przebiegła pomyślnie')
            return redirect('user_page')


class UserChangeImage(View):
    template_name = 'user_page.html'

    def get(self, request):
        form = ChangeImageForm(request.user)

        context = {'action': 'image',
                   'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
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


class UserDelete(View):
    template_name = 'user_page.html'

    def get(self, request):
        context = {'action': 'delete'}

        return render(request, self.template_name, context)

    def post(self, request):
        request.user.delete()
        messages.success(request, 'Konto zostało usunięte')
        return redirect('login')
