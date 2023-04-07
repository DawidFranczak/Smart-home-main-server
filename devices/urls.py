from django.urls import path

from .views import DeviceAdd, DevicesCardDelete, DevicesDelete, DevicesGetAll

urlpatterns = [
    path("", DevicesGetAll.as_view(), name="devices"),
    path("<int:pk>/delete", DevicesDelete.as_view(), name="device_delete"),
    path(
        "<int:pk>/delete/card", DevicesCardDelete.as_view(), name="device_card_delete"
    ),
    path("add", DeviceAdd.as_view(), name="device_add"),
]
