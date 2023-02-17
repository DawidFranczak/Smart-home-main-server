from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('rolety/', views.sunblind, name="sunblind"),
    path('rolety/kaibracja/<int:pk>', views.calibration, name="calibration"),
]
