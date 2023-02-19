from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
import json

from .mod import change_light

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

            # Simulation turn on/off light
            if sensor.name == 'tester':
                light = sensor.light
                if light.light:
                    light.light = False
                    response = {'response': 0}

                else:
                    light.light = True
                    response = {'response': 1}
                light.save()

                return JsonResponse(response)
            # End simulation

            return JsonResponse(change_light(sensor))
