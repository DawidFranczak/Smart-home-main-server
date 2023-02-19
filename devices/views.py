from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from .mod import add_uid, add_sensor, delete_sensor
# Create your views here.
from django.views import View


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
                    'cards': [
                        {'id': card.id,
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
                return JsonResponse({'response': 'Wybacz akurat tego czujnika nie można dodać w wersji testowej'})

            sensor = request.user.sensor_set.create(name=get_data['name'],
                                                    ip='111.111.111.111',
                                                    port=1234, fun=get_data['fun'])
            return JsonResponse({'response': 'Udało sie dodać czujnik', 'id': sensor.id})
        # End simulation

        elif get_data['fun'] == 'uid':
            return JsonResponse(add_uid(get_data, request.user))
        else:
            return JsonResponse(add_sensor(get_data, request.user))

    def delete(self, request):
        get_data = json.loads(request.body)
        return JsonResponse(delete_sensor(get_data, request.user))
