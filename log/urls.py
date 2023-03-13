from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import UserLogin, Home, UserRegister, UserLogout
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(Home.as_view(), login_url='login'), name="home"),
    path('zaloguj/', UserLogin.as_view(), name="login"),
    path('wyloguj/', login_required(UserLogout.as_view(),
         login_url='login'), name="logout"),
    path('rejestracja/', UserRegister.as_view(),  name="user_register"),

]
