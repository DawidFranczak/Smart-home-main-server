from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from .forms import CreateUserForm

# Create your views here.


class UserRegister(SuccessMessageMixin, CreateView):
    model = User
    form_class = CreateUserForm
    template_name = "register.html"
    success_url = "/zaloguj/"
    success_message = _("Registration was successful.")


class UserLogin(View):
    template = "login.html"

    def get(self, request):
        return render(request, self.template, status=200)

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username == "" or password == "":
            messages.error(request, _("Please fill all fields."))
            return render(request, self.template, status=404)

        if not User.objects.filter(username=username).exists():
            messages.error(request, _("User doesn't exists."))
            return render(request, self.template, status=404)

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, _("Incorrect name or password."))
            return render(request, self.template, status=401)

        login(request, user)
        return redirect("home")


class Home(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["image"] = self.request.user.homenavimage
        return context


class UserLogout(View):
    def get(self, request):
        logout(request)
        return redirect("login")


def handling_404(request, exception):
    print(exception)
    return render(request, "404.html", {}, status=404)
