from django.urls import path
from . import views

urlpatterns = [
    path('akwarium/<str:pk>',views.getAqua, name="getAqua"),
]