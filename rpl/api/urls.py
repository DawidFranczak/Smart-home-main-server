from django.urls import path

from .views import check_lamp, check_uid, get_lamp

urlpatterns = [
    path("uid/", check_uid, name="check_uid"),
    path("lamp/", check_lamp, name="check_lamp"),
    path("lamp/get/<int:id>/", get_lamp, name="get_lamp"),
]
