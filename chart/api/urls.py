from django.urls import path

from .views import sensor_get_all, sensor_update

urlpatterns = [
    path("all/", sensor_get_all, name="sensor_get_all"),
    path("update/", sensor_update, name="sensor_update"),
]
