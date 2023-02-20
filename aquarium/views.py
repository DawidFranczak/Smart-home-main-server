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
        device = request.user.device_set.get(pk=get_data['id'])
        aqua = device.aqua
        message = ""
        response = {}

        match get_data['action']:
            case 'changeRGB':
                red = str(get_data['r'])
                green = str(get_data['g'])
                blue = str(get_data['b'])
                message = f'r{red}g{green}b{blue}'
                aqua.color = message

            case 'changeLedTime':
                aqua.led_start = get_data['ledStart']
                aqua.led_stop = get_data['ledStop']

            case 'changeFluoLampTime':
                aqua.fluo_start = get_data['fluoLampStart']
                aqua.fluo_stop = get_data['fluoLampStop']

            case 'changeMode':
                aqua.mode = get_data['mode']  # True -> manual
                if get_data['mode']:
                    response = {
                        'fluo': aqua.fluo_mode,
                        'led': aqua.led_mode
                    }
                    aqua.save()
                    return JsonResponse(response)
                aqua.save()

            case 'changeFluoLampState':
                # True -> on
                message = 's1' if get_data['value'] else 's0'
                aqua.fluo_mode = get_data['value']

            case 'changeLedState':
                # True -> on
                message = 'r1' if get_data['value'] else 'r0'
                aqua.led_mode = get_data['value']

        if message:

            # Control simulation
            if device.name == 'tester':
                response = {'success': True,
                            'message': 'Udało się zmienić ustawienia'}
                aqua.save()
                return JsonResponse(response)
            # End simulation

            if send_data(message, device.ip, device.port):
                response = {'message': 'Udało się zmienić ustawienia'}
                aqua.save()
            else:
                response = {'message': 'Brak komunikacji z akwarium'}
        else:

            # Control simulation
            if device.name == 'tester':
                response = {'message': 'Udało się zmienić ustawienia'}
                aqua.save()
                return JsonResponse(response)
            # End simulation

            if check_aqua(device, aqua):
                response = {'message': 'Udało się zmienić ustawienia'}
                aqua.save()
            else:
                response = {'message': 'Brak komunikacji z akwarium'}

        return JsonResponse(response)

    aquas = request.user.device_set.filter(fun='aqua')
    print('********************************************')
    print(aquas)
    print('********************************************')

    context = {
        'aquas': aquas
    }
    return render(request, 'aquarium.html', context)
