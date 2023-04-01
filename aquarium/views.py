import json

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views import View

from .mod import aquarium_contorler
from .tester import aquarium_contorler_tester

# Create your views here.


class AquariumView(View):
    template_name = "aquarium.html"

    def get(self, request):
        aquas = request.user.sensor_set.filter(fun="aqua")
        context = {
            "aquas": aquas,
        }
        return render(request, self.template_name, context, status=200)

    def post(self, request):
        get_data = json.loads(request.body)
        sensor = request.user.sensor_set.get(pk=get_data["id"])

        # Control simulation
        if sensor.name == "tester":
            response = aquarium_contorler_tester(request, sensor.aqua)
            return JsonResponse(response, status=200)
        # End simulation

        response, status = aquarium_contorler(request, sensor)

        return JsonResponse(response, status=status)
