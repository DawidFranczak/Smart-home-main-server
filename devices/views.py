from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

import json

from .mod import add_uid, add_sensor, delete_sensor, add_sensor_tester


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
            message, status = add_sensor_tester(get_data, request)
            return JsonResponse(message, status=status)
        # End simulation

        if get_data['fun'] == 'uid':
            message, status = add_uid(get_data, request.user)
        else:
            message, status = add_sensor(get_data, request.user)

        return JsonResponse(message, status=status)

    def delete(self, request):
        get_data = json.loads(request.body)
        message, status = delete_sensor(get_data, request.user)
        return JsonResponse(message, status=status)
