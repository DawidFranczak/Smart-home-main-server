from django.urls import path
from . import views

urlpatterns = [
    path("uid/",views.checkUID, name = "checkUID"),
    path("lamp/",views.checkLamp, name = "checkLamp")
]

