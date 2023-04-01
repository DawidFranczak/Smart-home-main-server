import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from devices.models import Sensor

from .mod import stairs_settings

# Create your views here.


class StairsView(View):
    template_name = "stairs.html"

    def get(self, request):
        sensors = request.user.sensor_set.filter(fun="stairs")
        context = {
            "sensors": sensors,
        }
        return render(request, self.template_name, context)

    def post(self, request) -> JsonResponse:
        get_data = json.loads(request.body)

        sensor = get_object_or_404(Sensor, pk=get_data["id"])
        stairs = sensor.stairs
        ngrok = request.user.ngrok.ngrok
        message, status = stairs_settings(get_data, sensor, stairs, ngrok)

        return JsonResponse(message, status=status)
