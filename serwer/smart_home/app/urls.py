from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path('login/',views.login_user, name="login"),
    path('logout/',views.logout_user, name="logout"),
    path('light/',views.light, name="light"),
    path('wykres/',views.chart, name="chart"),
    path('sensor/',views.sensor, name="sensor"),
    path('schody/',views.stairs, name="stairs"),
    path('akwarium/',views.aquarium, name="aquarium"),
    path('rolety/',views.sunblind, name="sunblind"),
    path('rolety/kaibracja/<int:pk>',views.calibration, name="calibration"),
    path('rpl/',views.rpl, name="rpl"),
    path('rejestracja/',views.register_user, name="userRegister"),
    path('panel/',views.user_page, name="userPage"),
    path('zmiana-hasla',views.user_change_password, name="userChangePassword"),
    path('zmiana-emaila',views.user_change_email, name="userChangeEmail"),
    path('zmiana-zdjec',views.user_change_image, name="userChangeImage")
]
