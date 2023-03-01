from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import AquariumView

urlpatterns = [
    # path('akwarium/', views.aquarium, name="aquarium"),
    path('', AquariumView.as_view(), name="aquarium"),
]
