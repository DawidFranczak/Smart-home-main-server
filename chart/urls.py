from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import Chart

urlpatterns = [
    path("", login_required(Chart.as_view(), login_url="login"), name="chart"),
]
