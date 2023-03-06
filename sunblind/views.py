from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
import requests
import json

from app.const import MESSAGE_SUNBLIND

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
        ngrok = request.user.ngrok.ngrok
        # Simulation sunblind
        if sensor.name == 'tester':
            sunblind = sensor.sunblind
            sunblind.value = get_data['value']
            sunblind.save()
            return JsonResponse({'success': 1})
        # End simulation

        data = {
            "message": message,
            "ip": sensor.ip,
            "port": sensor.port,
        }
        try:
            answer = requests.put(ngrok + MESSAGE_SUNBLIND, data=data).json()
        except:
            return JsonResponse({'success': False,
                                 'message': "Brak komunikacji z serwerem w domu"})
        # Sending message to microcontroller and waiting on response
        if answer:
            sunblind = sensor.sunblind
            sunblind.value = get_data['value']
            sunblind.save()
        return JsonResponse({'success': answer,
                             'message': "" if answer else 'Brak komunikacji'})


class CalibrationView(View):
    template_name = 'calibration.html'

    def get(self, request, pk):
        sensor = request.user.sensor_set.get(pk=pk)
        send_data('calibration', sensor.ip, sensor.port)

        return render(request, self.template_name)

    def post(self, request, pk):
        sensor = request.user.sensor_set.get(id=pk)
        ngrok = request.user.ngrok.ngrok

        # Sending 'up', 'down' or 'stop' message to microcontroller
        get_data = json.loads(request.body)
        data = {
            "message": get_data['action'],
            "ip": sensor.ip,
            "port": sensor.port,
        }
        answer = requests.put(ngrok + MESSAGE_SUNBLIND, data=data).json()

        # Ending calibration, set value to 100 and save in database
        if get_data['action'] == 'end' and answer:

            sunblind = sensor.sunblind
            sunblind.value = 100
            sunblind.save()

        return JsonResponse(status=200, data={'success': answer, })
