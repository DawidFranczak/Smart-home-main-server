from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
import requests
import json

from app.const import CHANGE_STAIRS
# Create your views here.


class StairsView(View):
    template_name = 'stairs.html'

    def get(self, request):
        sensors = request.user.sensor_set.filter(fun='stairs')
        context = {
            "sensors": sensors,
        }
        return render(request, self.template_name, context)

    def post(self, request) -> JsonResponse:
        get_data = json.loads(request.body)

        sensor = request.user.sensor_set.get(pk=get_data['id'])
        stairs = sensor.stairs
        ngrok = request.user.ngrok.ngrok

        match get_data['action']:
            case 'set-lightingTime':

                stairs.lightTime = int(get_data['lightingTime'])
                message = 'te'+str(get_data['lightingTime'])

            case 'set-brightness':

                stairs.brightness = int(get_data['brightness'])
                message = 'bs'+str(get_data['brightness'])

            case 'set-step':

                stairs.steps = int(get_data['step'])
                message = 'sp'+str(get_data['step'])

            case 'change-stairs':

                if stairs.mode:
                    stairs.mode = False
                    message = 'OFF'
                else:
                    stairs.mode = True
                    message = 'ON'

        # Control simulation
        if sensor.name == 'tester':
            stairs.save()
            return JsonResponse({'respond': "Udało się zmienić ustawienia"})
        # End simulation

        data = {
            "message": message,
            "ip": sensor.ip,
            "port": sensor.port,
        }
        try:
            answer = requests.put(ngrok+CHANGE_STAIRS, data=data).json()
        except:
            return JsonResponse({'respond': "Brak komunikacji z serwerem w domu"})
        if answer:
            stairs.save()
        return JsonResponse({'respond': "Udało się zmienić ustawienia"
                             if answer else "Brak komunikacji ze schodami"})
