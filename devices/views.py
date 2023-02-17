from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from .mod import add_uid, add_sensor, delete_sensor
# Create your views here.


@login_required(login_url='login')
def devices(request):
    user_id = request.user.id

    match request.method:
        case 'POST':
            get_data = json.loads(request.body)

            # Simulation adding sensors
            if get_data['name'] == 'tester':
                EXCLUDED_SENSORS = ['temp', 'rfid', 'button', 'lamp', 'uid']

                if get_data['fun'] in EXCLUDED_SENSORS:
                    return JsonResponse({'response': 'Wybacz akurat tego czujnika nie można dodać w wersji testowej'})

                sensor = request.user.sensor_setcreate(name=get_data['name'],
                                                       ip='111.111.111.111',
                                                       port=1234, fun=get_data['fun'],
                                                       user_id=user_id)
                return JsonResponse({'response': 'Udało sie dodać czujnik', 'id': sensor.id})
            # End simulation

            elif get_data['action'] == 'add' and get_data['fun'] == 'uid':
                return JsonResponse(add_uid(get_data))
            else:
                return JsonResponse(add_sensor(get_data, user_id))

        case 'DELETE':
            get_data = json.loads(request.body)
            return JsonResponse(delete_sensor(get_data))

        case 'GET':

            sensors = request.user.sensor_set.filter(user=request.user)

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
