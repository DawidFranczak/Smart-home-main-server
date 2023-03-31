from django.urls import path
from .views import RplView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", login_required(RplView.as_view(), login_url="login"), name="rpl"),
]
