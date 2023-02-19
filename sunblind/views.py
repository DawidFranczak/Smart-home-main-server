from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
import json
from .mod import send_data

# Create your views here.


class SunblindView(View):
    template_name = 'sunblind.html'

    def get(self, request):
        # Getting all user sensor where function is sunblind
        sensors = request.user.sensor_set.filter(fun='sunblind')

        context = {
            'sensors': [{
                        'id': sensor.id,
                        'name': sensor.name,
                        'value': sensor.sunblind.value
                        } for sensor in sensors]
        }
        return render(request, self.template_name, context)

    def post(self, request) -> JsonResponse:
        get_data = json.loads(request.body)
        sensor = request.user.sensor_set.get(pk=get_data['id'])
        message = 'set' + str(get_data['value'])

        # Simulation sunblind
        if sensor.name == 'tester':
            sunblind = sensor.sunblind
            sunblind.value = get_data['value']
            sunblind.save()
            return JsonResponse({'success': 1})
        # End simulation

        # Sending message to microcontroller and waiting on response
        if send_data(message, sensor.ip, sensor.port):
            sunblind = sensor.sunblind
            sunblind.value = get_data['value']
            sunblind.save()
            return JsonResponse({'success': 1})
        else:
            return JsonResponse({'message': 'Brak komunikacji'})


class CalibrationView(View):
    template_name = 'calibration.html'

    def get(self, request, pk):
        sensor = request.user.sensor_set.get(pk=pk)
        send_data('calibration', sensor.ip, sensor.port)

        return render(request, self.template_name)

    def post(self, request, pk):
        sensor = request.user.sensor_set.get(id=pk)

        # Sending 'up', 'down' or 'stop' message to microcontroller
        get_data = json.loads(request.body)
        send_data(get_data['action'], sensor.ip, sensor.port)

        # Ending calibration, set value to 100 and save in database
        if get_data['action'] == 'end':
            sunblind = sensor.sunblind
            sunblind.value = 100
            sunblind.save()
