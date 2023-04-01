from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import LightView

urlpatterns = [
    path("", login_required(LightView.as_view(), login_url="login"), name="light"),
]
