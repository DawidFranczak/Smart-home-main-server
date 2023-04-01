import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from devices.models import Sensor

from .mod import change_light, change_light_tester

# Create your views here.


class LightView(View):
    template_name = "light.html"

    def get(self, request):
        sensors = request.user.sensor_set.filter(fun="light")

        context = {
            "sensors": [
                {"id": sensor.id, "name": sensor.name, "light": sensor.light.light}
                for sensor in sensors
            ]
        }

        return render(request, self.template_name, context, status=200)

    def post(self, request):
        get_data = json.loads(request.body)

        if get_data["action"] == "change":
            sensor = get_object_or_404(Sensor, pk=get_data["id"])
            ngrok = request.user.ngrok.ngrok

            # Simulation turn on/off light
            if sensor.name == "tester":
                message = change_light_tester(sensor)
                return JsonResponse(message, status=200)
            # End simulation

            message, status = change_light(sensor, ngrok)
            return JsonResponse(message, status=status)
        return JsonResponse({}, status=404)
