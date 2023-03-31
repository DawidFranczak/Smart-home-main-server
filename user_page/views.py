from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from log.models import Ngrok
from .models import HomeNavImage

from .forms import ChangePasswordForm, ChangeEmailForm, ChangeImageForm, ChangeNgrokForm

# Create your views here.


class UserPage(TemplateView):
    template_name = "user_page.html"


class UserChangePassword(View):
    template_name = "user_page.html"
    form_class = ChangePasswordForm

    def get(self, request):
        context = {"action": "password", "form": ChangePasswordForm(request.user)}

        return render(request, self.template_name, context, status=200)

    def post(self, request):
        form = self.form_class(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _("Password successfully updated"))
            return redirect("user_page")

        context = {"action": "password", "form": form}

        return render(request, self.template_name, context, status=200)


class UserChangeEmail(SuccessMessageMixin, UpdateView):
    model = User
    success_message = _("Email successfully updated")
    form_class = ChangeEmailForm
    success_url = "/ustawienia/"
    template_name = "user_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "email"
        return context


class UserChangeNgrok(SuccessMessageMixin, UpdateView):
    model = Ngrok
    form_class = ChangeNgrokForm
    success_url = "/ustawienia/"
    template_name = "user_page.html"
    success_message = _("URL successfully updated")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "ngrok"
        return context


class UserChangeImage(SuccessMessageMixin, UpdateView):
    template_name = "user_page.html"
    model = HomeNavImage
    form_class = ChangeImageForm
    success_url = "/ustawienia/"
    success_message = _("Image(s) sccessfully updated")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "image"
        return context


class UserChangeImageReset(View):
    def get(self, request):
        user_image = request.user.homenavimage
        user_image.home = "images/home.png"
        user_image.rpl = "images/rfid.png"
        user_image.aquarium = "images/aqua.png"
        user_image.sunblind = "images/sunblind.png"
        user_image.temperature = "images/temp.png"
        user_image.profile = "images/user.png"
        user_image.light = "images/lamp.png"
        user_image.stairs = "images/stairs.png"
        user_image.sensor = "images/sensor.png"
        user_image.logout = "images/logout.png"
        user_image.save()
        messages.success(request, _("Images reseted"))

        return redirect("user_page")


class UserDelete(SuccessMessageMixin, DeleteView):
    model = User
    success_message = _("Account has deleted")
    success_url = "/zaloguj/"
    template_name = "user_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "delete"
        return context
