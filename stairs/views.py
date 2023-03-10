from django.utils.translation import gettext as _
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
import requests
import json

from app.const import CHANGE_STAIRS
from devices.models import Sensor
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

        # sensor = request.user.sensor_set.get(pk=get_data['id'])
        sensor = get_object_or_404(Sensor, pk=get_data['id'])
        stairs = sensor.stairs
        ngrok = request.user.ngrok.ngrok

        match get_data['action']:
            case 'set-lightingTime':

                stairs.lightTime = int(get_data['lightingTime'])
                message = 'te'+str(get_data['lightingTime'])
                field = "lightTime"

            case 'set-brightness':

                stairs.brightness = int(get_data['brightness'])
                message = 'bs'+str(get_data['brightness'])
                field = "brightness"

            case 'set-step':

                stairs.steps = int(get_data['step'])
                message = 'sp'+str(get_data['step'])
                field = "steps"

            case 'change-stairs':
                field = "mode"

                if stairs.mode:
                    stairs.mode = False
                    message = 'OFF'
                else:
                    stairs.mode = True
                    message = 'ON'

        # Control simulation
        if sensor.name == 'tester':
            stairs.save(update_fields=[field])
            return JsonResponse({'respond': _('Settings updated successfully')}, status=200)
        # End simulation

        data = {
            "message": message,
            "ip": sensor.ip,
            "port": sensor.port,
        }
        try:
            answer = requests.put(ngrok+CHANGE_STAIRS, data=data).json()
        except:
            return JsonResponse({'respond': _("No connection with home server.")}, status=500)

        message = {'respond': _('No connection with stairs')}
        status = 500

        if answer:
            stairs.save(update_fields=[field])
            message = {'respond': _('Settings updated successfully')}
            status = 200
        return JsonResponse(message, status=status)
