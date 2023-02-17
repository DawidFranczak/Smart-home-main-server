from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

from .mod import *

# Create your views here.


@login_required(login_url='login')
def aquarium(request):
    if request.method == "POST":
        get_data = json.loads(request.body)
        sensor = request.user.sensor_set.get(pk=get_data['id'])
        aqua = sensor.aqua
        message = ""
        response = {}

        match get_data['action']:
            case 'changeRGB':
                message = 'r'+str(get_data['r'])+'g' + \
                    str(get_data['g'])+'b'+str(get_data['b'])
                aqua.color = message

            case 'changeLedTime':
                aqua.led_start = get_data['ledStart']
                aqua.led_stop = get_data['ledStop']

            case 'changeFluoLampTime':
                aqua.fluo_start = get_data['fluoLampStart']
                aqua.fluo_stop = get_data['fluoLampStop']

            case 'changeMode':
                aqua.mode = get_data['mode']
                if get_data['mode']:
                    response = {
                        'fluo': aqua.fluo_mode,
                        'led': aqua.led_mode
                    }
                    aqua.save()
                    return JsonResponse(response)
                else:
                    aqua.save()

            case 'changeFluoLampState':
                if get_data['value']:
                    message = 's1'
                else:
                    message = 's0'
                aqua.fluo_mode = get_data['value']

            case 'changeLedState':
                if get_data['value']:
                    message = 'r1'
                else:
                    message = 'r0'
                aqua.led_mode = get_data['value']

        if message:

            # Control simulation
            if sensor.name == 'tester':
                response = {'success': True,
                            'message': 'Udało się zmienić ustawienia'}
                aqua.save()
                return JsonResponse(response)
            # End simulation

            if send_data(message, sensor.ip, sensor.port):
                response = {'message': 'Udało się zmienić ustawienia'}
                aqua.save()
            else:
                response = {'message': 'Brak komunikacji z akwarium'}
        else:

            # Control simulation
            if sensor.name == 'tester':
                response = {'message': 'Udało się zmienić ustawienia'}
                aqua.save()
                return JsonResponse(response)
            # End simulation

            if check_aqua(sensor, aqua):
                response = {'message': 'Udało się zmienić ustawienia'}
                aqua.save()
            else:
                response = {'message': 'Brak komunikacji z akwarium'}

        return JsonResponse(response)

    aquas = request.user.sensor_set.filter(fun='aqua')
    context = {
        'aquas': aquas
    }
    return render(request, 'aquarium.html', context)
