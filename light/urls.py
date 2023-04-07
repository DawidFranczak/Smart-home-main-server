from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import LightGetAll, LightUpdate

urlpatterns = [
    path("", LightGetAll.as_view(), name="light"),
    path("update/", LightUpdate.as_view(), name="light_update"),
]
