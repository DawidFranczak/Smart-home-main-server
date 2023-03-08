from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.utils.translation import gettext as _
from django.contrib.auth import update_session_auth_hash

from .forms import ChangePasswordForm, ChangeEmailForm, ChangeImageForm, ChangeNgrokForm

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
            messages.success(request, _("Password successfully updated"))
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
        form = self.form_class(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, _("Email successfully updated"))
            return redirect('user_page')

        old = request.user.email
        context = {'action': 'email',
                   'form': form,
                   'old': old}
        return render(request, self.template_name, context)


class UserChangeNgrok(View):
    template_name = 'user_page.html'
    form_class = ChangeNgrokForm

    def get(self, request):
        form = self.form_class(request.user)

        old = request.user.ngrok.ngrok

        context = {'action': 'ngrok',
                   'form': form,
                   'old': old}

        return render(request, self.template_name, context)

    def post(self, request):
        form = ChangeNgrokForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("URL successfully updated"))
            return redirect('user_page')

        old = request.user.ngrok.ngrok
        form = ChangeNgrokForm(request.user, request.POST)
        context = {'action': 'ngrok',
                   'form': form,
                   'old': old}
        print(form)

        return render(request, self.template_name, context)


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
                messages.success(request, _("Image(s) sccessfully updated"))
                return redirect('user_page')

            context = {'action': 'image',
                       'form': form}
            return render(request, self.template_name, context)
        else:
            form.reset(request.user)
            messages.success(request, _("Images reseted"))
            return redirect('user_page')


class UserDelete(View):
    template_name = 'user_page.html'

    def get(self, request):
        context = {'action': 'delete'}

        return render(request, self.template_name, context)

    def post(self, request):
        request.user.delete()
        messages.success(request, _("Account has deleted"))
        return redirect('login')
