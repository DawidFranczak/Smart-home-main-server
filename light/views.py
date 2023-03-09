from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
import json

from .mod import change_light
from app.const import CHANGE_LIGHT
# Create your views here.


class LightView(View):
    template_name = 'light.html'

    def get(self, request):
        sensors = request.user.sensor_set.filter(fun='light')

        context = {
            'sensors': [
                {'id': sensor.id,
                 'name': sensor.name,
                 'light': sensor.light.light
                 } for sensor in sensors
            ]
        }

        return render(request, self.template_name, context)

    def post(self, request):
        get_data = json.loads(request.body)

        if get_data['action'] == 'change':
            id = get_data['id']
            sensor = request.user.sensor_set.get(pk=id)
            ngrok = request.user.ngrok.ngrok

            # Simulation turn on/off light
            if sensor.name == 'tester':
                light = sensor.light
                if light.light:
                    light.light = False
                    response = {'response': "OFF"}

                else:
                    light.light = True
                    response = {'response': "ON"}
                light.save(update_fields=["light"])
                return JsonResponse(response, status=200)
            # End simulation
            message, status = change_light(sensor, ngrok)
            return JsonResponse(message, status=status)
