import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import TemplateView

from devices.models import Sensor

from .mod import (
    sunblind_calibrations,
    sunblind_calibrations_tester,
    sunblind_move,
    sunblind_move_tester,
)


class SunblindLoginRequired(LoginRequiredMixin):
    login_url = "login"


class SunblindGetAll(SunblindLoginRequired, TemplateView):
    """
    This class give all user's sunblind

    endpoint: rolety/
    """

    template_name = "sunblind.html"

    def get_context_data(self):
        sensors = self.request.user.sensor_set.filter(fun="sunblind")

        return {
            "sensors": [
                {"id": sensor.id, "name": sensor.name, "value": sensor.sunblind.value}
                for sensor in sensors
            ]
        }


class SunblindUpdate(SunblindLoginRequired, View):
    """
    This class move selected sunblind

    endpoint: rolety/update
    """

    def put(self, request) -> JsonResponse:
        get_data = json.loads(request.body)
        sensor = get_object_or_404(Sensor, pk=get_data["id"])
        ngrok = request.user.ngrok.ngrok
        value: int = get_data["value"]

        # Simulation sunblind
        if sensor.name == "tester":
            sunblind_move_tester(sensor, value)
            return JsonResponse({}, status=204)
        # End simulation

        message, status = sunblind_move(ngrok, sensor, value)
        return JsonResponse(message, status=status)


class CalibrationGet(SunblindLoginRequired, TemplateView):
    """
    This class start sunblind's calibration

    endpoint: rolety/<int:id>
    """

    template_name = "calibration.html"

    def get_context_data(self, pk):
        sensor = get_object_or_404(Sensor, pk=pk)
        ngrok = self.request.user.ngrok.ngrok
        sunblind_calibrations(ngrok, sensor, "calibration")
        return super().get_context_data()


class CalibrationUpdate(SunblindLoginRequired, View):
    """
    This class start sends commands (up/down/stop)

    endpoint: rolety/<int:id>/update
    """

    def put(self, request, pk):
        sensor = get_object_or_404(Sensor, pk=pk)
        ngrok = request.user.ngrok.ngrok

        get_data = json.loads(request.body)
        action: str = get_data["action"]

        # Simulation calibration
        if sensor.name == "tester":
            sunblind_calibrations_tester(sensor)
            return JsonResponse({"success": True}, status=200)
        # End simulation

        answer, status = sunblind_calibrations(ngrok, sensor, action)

        return JsonResponse({"success": answer}, status=status)
