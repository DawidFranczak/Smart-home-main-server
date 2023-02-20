from django.urls import path
from . import views

urlpatterns = [
    path('schody/<str:pk>', views.getStairs, name="getStairs"),
]
