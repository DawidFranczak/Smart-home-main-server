from django.urls import path
from . import views

urlpatterns = [
    path("uid/", views.check_UID, name="check_UID"),
    path("lamp/", views.check_lamp, name="check_lamp")
]
