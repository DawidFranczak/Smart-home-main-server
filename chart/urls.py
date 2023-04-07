from django.urls import path

from .views import ChartGetData

urlpatterns = [
    path("", ChartGetData.as_view(), name="chart"),
]
