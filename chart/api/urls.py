from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.getSensorAll, name="getSensorAll"),
    path('update/', views.updateSensor, name="updateSensor"),

]
