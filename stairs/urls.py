from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import StairsView

urlpatterns = [
    path('schody/', login_required(StairsView.as_view(),
         login_url='login'), name="stairs"),

]
