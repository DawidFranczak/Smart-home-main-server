from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import Home, UserLogin, UserLoginCheck, UserLogout, UserRegister

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("zaloguj/", UserLogin.as_view(), name="login"),
    path("zaloguj/check", UserLoginCheck.as_view(), name="login_check"),
    path(
        "wyloguj/",
        UserLogout.as_view(),
        name="logout",
    ),
    path("rejestracja/", UserRegister.as_view(), name="user_register"),
]
