from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import AquariumView

urlpatterns = [
    path(
        "", login_required(AquariumView.as_view(), login_url="login"), name="aquarium"
    ),
]
