from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import DevicesView

urlpatterns = [
    path("", login_required(DevicesView.as_view(), login_url="login"), name="devices"),
]
