from django.urls import path
from .views import LightView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(LightView.as_view(),
         login_url='login'), name="light"),

]
