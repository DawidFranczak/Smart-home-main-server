from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import gettext as _

from .mod import data_for_chart

# Create your views here.


@login_required(login_url="login")
def chart(request):
    template_name = "chart.html"

    if request.method == "POST" or request.method == "GET":
        list_place = request.user.sensor_set.filter(fun="temp")

        if len(list_place) == 0:
            context = {"list_place": [_("No sensors have been added")]}
            return render(request, template_name, context, status=404)

        context = data_for_chart(request, list_place)
        return render(request, template_name, context, status=200)

    return render(request, template_name, status=405)
