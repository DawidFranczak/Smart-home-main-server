import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from devices.models import Sensor

from .mod import (
    sunblind_calibrations,
    sunblind_calibrations_tester,
    sunblind_move,
    sunblind_move_tester,
)

# Create your views here.


class SunblindView(View):
    template_name = "sunblind.html"

    def get(self, request):
        # Getting all user sensor where function is sunblind
        sensors = request.user.sensor_set.filter(fun="sunblind")

        context = {
            "sensors": [
                {"id": sensor.id, "name": sensor.name, "value": sensor.sunblind.value}
                for sensor in sensors
            ]
        }
        return render(request, self.template_name, context, status=200)

    def post(self, request) -> JsonResponse:
        get_data = json.loads(request.body)
        sensor = get_object_or_404(Sensor, pk=get_data["id"])
        ngrok = request.user.ngrok.ngrok
        value: int = get_data["id"]

        # Simulation sunblind
        if sensor.name == "tester":
            sunblind_move_tester(sensor, value)
            return JsonResponse({}, status=204)
        # End simulation

        message, status = sunblind_move(ngrok, sensor, value)
        return JsonResponse(message, status=status)


class CalibrationView(View):
    template_name = "calibration.html"

    def get(self, request, pk):
        get_object_or_404(Sensor, pk=pk)
        return render(request, self.template_name, status=200)

    def post(self, request, pk):
        sensor = get_object_or_404(Sensor, pk=pk)
        ngrok = request.user.ngrok.ngrok

        # Sending 'up', 'down' or 'stop' message to microcontroller
        get_data = json.loads(request.body)
        action: str = get_data["action"]

        # Simulation calibration
        if sensor.name == "tester":
            sunblind_calibrations_tester(sensor)
            return JsonResponse({"success": True}, status=200)
        # End simulation

        answer, status = sunblind_calibrations(ngrok, sensor, action)

        return JsonResponse({"success": answer}, status=status)
