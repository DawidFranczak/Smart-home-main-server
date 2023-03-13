from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
import requests
import json

from app.const import MESSAGE_SUNBLIND
from devices.models import Sensor
from .mod import sunblind_move, sunblind_move_tester, sunblind_calibrations, sunblind_calibrations_tester
# Create your views here.


class SunblindView(View):
    template_name = 'sunblind.html'

    def get(self, request):
        # Getting all user sensor where function is sunblind
        sensors = request.user.sensor_set.filter(fun='sunblind')

        context = {
            'sensors': [
                {
                    'id': sensor.id,
                    'name': sensor.name,
                    'value': sensor.sunblind.value
                }
                for sensor in sensors]
        }
        return render(request, self.template_name, context, status=200)

    def post(self, request) -> JsonResponse:
        get_data = json.loads(request.body)
        sensor = get_object_or_404(Sensor, pk=get_data['id'])
        ngrok = request.user.ngrok.ngrok

        # Simulation sunblind
        if sensor.name == 'tester':
            sunblind_move_tester(sensor, get_data)
            return JsonResponse({}, status=204)
        # End simulation

        message, status = sunblind_move(ngrok, sensor, get_data)
        return JsonResponse(message, status=status)


class CalibrationView(View):
    template_name = 'calibration.html'

    def get(self, request, pk):
        get_object_or_404(Sensor, pk=pk)
        return render(request, self.template_name, status=200)

    def post(self, request, pk):

        sensor = get_object_or_404(Sensor, pk=pk)
        ngrok = request.user.ngrok.ngrok

        # Sending 'up', 'down' or 'stop' message to microcontroller
        get_data = json.loads(request.body)

        # Simulation calibration
        if sensor.name == "tester":
            sunblind_calibrations_tester(sensor)
            return JsonResponse(status=200, data={'success': True})
        # End simulation

        answer, status = sunblind_calibrations(ngrok, sensor, get_data)

        return JsonResponse(status=status, data={'success': answer, })
