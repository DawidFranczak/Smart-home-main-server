from django.http import JsonResponse
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views import View

from .mod import aquarium_contorler
from .tester import check_aqua_testet

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
        # Control simulation
        if request.sensor.name == "tester":
            check_aqua_testet(request.sensor.aqua)
            message = {"message": _("Settings updated successfully")}
            return JsonResponse(message, status=200)
        # End simulation

        response = aquarium_contorler(request)

        message = _("No connection with aquarium")

        if response:
            message = _("Settings updated successfully")

        return JsonResponse({"message": message}, status=200)
