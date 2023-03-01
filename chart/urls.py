from django.urls import path
from .views import Chart
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', login_required(Chart.as_view(), login_url='login'), name="chart"),

]
