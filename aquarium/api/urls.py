from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>', views.getAqua, name="getAqua"),
    path('all/', views.getAquaAll, name="getAquaAll"),
    path('update/', views.updateAqua, name="updateAqua"),
]
