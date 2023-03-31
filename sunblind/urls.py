from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import SunblindView, CalibrationView

urlpatterns = [
    path(
        "", login_required(SunblindView.as_view(), login_url="login"), name="sunblind"
    ),
    path(
        "kaibracja/<int:pk>",
        login_required(CalibrationView.as_view(), login_url="login"),
        name="calibration",
    ),
]
