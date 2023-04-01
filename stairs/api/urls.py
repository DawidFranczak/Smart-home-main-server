from django.urls import path

from .views import get_stairs

urlpatterns = [
    path("<str:pk>", get_stairs, name="get_stairs"),
]
