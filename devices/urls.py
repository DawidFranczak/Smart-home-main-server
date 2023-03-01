from django.urls import path
from .views import DevicesView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(DevicesView.as_view(),
         login_url='login'), name="devices"),
]
