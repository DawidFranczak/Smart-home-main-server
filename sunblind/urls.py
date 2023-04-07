from django.urls import path

from .views import CalibrationGet, CalibrationUpdate, SunblindGetAll, SunblindUpdate

urlpatterns = [
    path("", SunblindGetAll.as_view(), name="sunblind"),
    path("update/", SunblindUpdate.as_view(), name="sunblind_update"),
    path(
        "kaibracja/<int:pk>",
        CalibrationGet.as_view(),
        name="calibration",
    ),
    path(
        "kaibracja/<int:pk>/update/",
        CalibrationUpdate.as_view(),
        name="calibration_update",
    ),
]
