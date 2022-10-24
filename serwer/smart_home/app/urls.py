from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path('login/',views.loginUser, name="login"),
    path('logout/',views.logoutUser, name="logout"),
    path('light/',views.light, name="light"),
    path('wykres/',views.wykres, name="wykres"),
    path('sensor/',views.sensor, name="sensor"),
    path('schody/',views.stairs, name="stairs"),
    path('akwarium/',views.akwarium, name="akwarium"),
    path('rolety/',views.rolety, name="rolety"),
    path('rolety/kaibracja/<int:pk>',views.calibration, name="calibration"),
    path('rpl/',views.rpl, name="rpl"),
    
]