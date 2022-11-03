from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path('login/',views.loginUser, name="login"),
    path('logout/',views.logoutUser, name="logout"),
    path('light/',views.light, name="light"),
    path('wykres/',views.chart, name="chart"),
    path('sensor/',views.sensor, name="sensor"),
    path('schody/',views.stairs, name="stairs"),
    path('akwarium/',views.aquarium, name="aquarium"),
    path('rolety/',views.sunblind, name="sunblind"),
    path('rolety/kaibracja/<int:pk>',views.calibration, name="calibration"),
    path('rpl/',views.rpl, name="rpl"),
    path('rejestracja/',views.registerUser, name="registerUser"),
    
]