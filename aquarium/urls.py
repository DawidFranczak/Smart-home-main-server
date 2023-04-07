from django.urls import path

from .views import AquariumGetAll, AquariumUpdate

urlpatterns = [
    path("", AquariumGetAll.as_view(), name="aquarium"),
    path("update/", AquariumUpdate.as_view(), name="aquarium_update"),
]
