import json
import requests
from app.const import CHANGE_AQUA, CHECK_AQUA
from .tester import check_aqua_testet
from .api.serialized import AquaSerializer


def change(message, sensor, ngrok) -> bool:
    """Return True if the communication with aqua is successful."""

    data = {
        'message': message,
        'ip': sensor.ip,
        'port': sensor.port
    }
    api = ngrok+CHANGE_AQUA
    # api = ngrok+'/api/aquarium/start'

    response = requests.post(api, data=data)
    response = response.json()['response']
    if response:
        sensor.aqua.save()
    return response


def check(sensor, ngrok) -> bool:
    """Return True if the communication with aqua is successful."""

    aqua = sensor.aqua
    settings = AquaSerializer(aqua, many=False).data
    settings['ip'] = sensor.ip
    settings['port'] = sensor.port
    api = ngrok+CHECK_AQUA
    response = requests.post(api, data=settings)

    response = response.json()
    success = response['response']

    if success:
        aqua.fluo_mode = response['fluo_mode']
        aqua.led_mode = response['led_mode']
        aqua.save()
    return success


def aquarium_contorler(request):

    get_data = json.loads(request.body)
    sensor = request.user.sensor_set.get(pk=get_data['id'])
    aqua = sensor.aqua
    ngrok = request.user.ngrok.ngrok
    response = True

    match get_data['action']:
        case 'changeRGB':
            red = str(get_data['r'])
            green = str(get_data['g'])
            blue = str(get_data['b'])
            message = f'r{red}g{green}b{blue}'
            response = change(message, sensor, ngrok)

        case 'changeLedTime':
            aqua.led_start = get_data['ledStart']
            aqua.led_stop = get_data['ledStop']
            response = check(sensor, ngrok)

        case 'changeFluoLampTime':
            aqua.fluo_start = get_data['fluoLampStart']
            aqua.fluo_stop = get_data['fluoLampStop']
            response = check(sensor, ngrok)

        case 'changeMode':
            aqua.mode = get_data['mode']  # True -> manual
            aqua.save()

            if get_data['mode']:  # maunal
                response = {
                    'fluo': aqua.fluo_mode,
                    'led': aqua.led_mode
                }
                return response
            response = check(sensor, ngrok)  # auto

        case 'changeFluoLampState':
            # True -> on
            message = 's1' if get_data['value'] else 's0'
            aqua.fluo_mode = get_data['value']
            response = change(message, sensor, ngrok)

        case 'changeLedState':
            # True -> on
            message = 'r1' if get_data['value'] else 'r0'
            aqua.led_mode = get_data['value']
            response = change(message, sensor, ngrok)

    # Control simulation
    if sensor.name == 'tester':
        response = check_aqua_testet(aqua)
    # End simulation

    return {'message': 'Udało się zmienić ustawienia' if response else 'Brak komunikacji z akwarium'}
