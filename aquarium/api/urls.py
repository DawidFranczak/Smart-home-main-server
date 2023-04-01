from django.urls import path

from .views import get_aqua, get_aqua_all, update_aqua

urlpatterns = [
    path("<int:pk>", get_aqua, name="get_aqua"),
    path("all/", get_aqua_all, name="get_aqua_all"),
    path("update/", update_aqua, name="update_aqua"),
]
