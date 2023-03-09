from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

import json

from .mod import add_uid, add_sensor, delete_sensor


class DevicesView(View):
    template_name = 'devices.html'

    def get(self, request):
        sensors = request.user.sensor_set.all()

        context = {
            'sensors': [
                {
                    'fun': sensor.fun,
                    'name': sensor.name,
                    'id': sensor.id,
                    'cards': [{
                        'id': card.id,
                        'name': card.name
                    } for card in sensor.card_set.all()
                    ] if sensor.fun == 'rfid' else ""
                } for sensor in sensors]
        }

        return render(request, 'devices.html', context)

    def post(self, request):
        get_data = json.loads(request.body)
        # Simulation adding sensors
        if get_data['name'] == 'tester':
            EXCLUDED_SENSORS = ['temp', 'rfid', 'button', 'lamp', 'uid']

            if get_data['fun'] in EXCLUDED_SENSORS:
                return JsonResponse({'response': _("Sorry, you can't add this type of device in the test version")}, status=200)

            sensor = request.user.sensor_set.create(name=get_data['name'],
                                                    ip='111.111.111.111',
                                                    port=1234, fun=get_data['fun'])
            return JsonResponse({'response': _("Device added successfully"), 'id': sensor.id}, status=200)
        # End simulation

        elif get_data['fun'] == 'uid':
            message, status = add_uid(get_data, request.user)
            return JsonResponse(message, status=status)
        else:
            message, status = add_sensor(get_data, request.user)
            return JsonResponse(message, status=status)

    def delete(self, request):
        get_data = json.loads(request.body)
        message, status = delete_sensor(get_data, request.user)
        return JsonResponse(message, status=status)
