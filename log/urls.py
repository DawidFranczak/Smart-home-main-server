from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('zaloguj/', views.user_login, name="login"),
    path('wyloguj/', views.user_logout, name="logout"),
    path('rejestracja/', views.user_register, name="user_register"),

]
