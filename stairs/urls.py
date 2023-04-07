from django.urls import path

from .views import StairsGetAll, StairsUpdate

urlpatterns = [
    path(
        "",
        StairsGetAll.as_view(),
        name="stairs",
    ),
    path("update/", StairsUpdate.as_view(), name="stairs_update"),
]
