from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
# Create your views here.


@login_required(login_url='login')
def rpl(request):
    if request.method == 'POST':
        get_data = json.loads(request.body)

        if get_data['action'] == 'get':
            lamp = request.user.sensor_set.get(pk=get_data['id'])

            rfids = request.user.sensor_set.filter(
                fun='rfid')
            buttons = request.user.sensor_set.filter(
                fun='btn')

            respond = {'rfid': [rfid.id for rfid in rfids if rfid.rfid.lamp == lamp.ip],
                       'btn': [button.id for button in buttons if button.button.lamp == lamp.ip]}

            return JsonResponse(respond)

        elif get_data['action'] == 'connect':

            lamp = request.user.sensor_set.get(pk=get_data['lamp'])

            SENSORS_RFID = request.user.sensor_set.filter(
                fun='rfid')
            CONNECTED_RFIDS = set([
                sensor.id for sensor in SENSORS_RFID if sensor.rfid.lamp == lamp.ip])
            ADD_RFIDS = set([int(rfid_id) for rfid_id in get_data['rfids']])

            CONNECT_RFIDS = ADD_RFIDS - CONNECTED_RFIDS
            REMOVE_RFIDS = CONNECTED_RFIDS - ADD_RFIDS

            SENSORS_BUTTON = request.user.sensor_set.filter(
                fun='btn')
            CONNECTED_BUTTONS = set([
                sensor.id for sensor in SENSORS_BUTTON if sensor.button.lamp == lamp.ip])
            ADD_BUTTON = set([int(button_id)
                              for button_id in get_data['btns']])

            CONNECT_BUTTONS = ADD_BUTTON - CONNECTED_BUTTONS
            REMOVE_BUTTONS = CONNECTED_BUTTONS - ADD_BUTTON

            for id in CONNECT_RFIDS:
                rfid = request.user.sensor_set.get(pk=id).rfid
                rfid.lamp = lamp.ip
                rfid.save()

            for id in REMOVE_RFIDS:
                rfid = request.user.sensor_set.get(pk=id).rfid
                rfid.lamp = ""
                rfid.save()

            for id in CONNECT_BUTTONS:
                btn = request.user.sensor_set.get(pk=id).btn
                btn.lamp = lamp.ip
                btn.save()

            for id in REMOVE_BUTTONS:
                btn = request.user.sensor_set.get(pk=id).btn
                btn.lamp = ""
                btn.save()

            message = {'message': 'Połączono'}
            return JsonResponse(message)

    rfids = request.user.sensor_set.filter(fun='rfid')
    lamps = request.user.sensor_set.filter(fun='lamp')
    buttons = request.user.sensor_set.filter(fun='btn')

    context = {'rfids': [{
        'id': rfid.id,
        'name': rfid.name} for rfid in rfids],
        'lamps': [{
            'id': lamp.id,
            'name': lamp.name} for lamp in lamps],
        'buttons': [{
            'id': button.id,
            'name': button.name} for button in buttons]}

    return render(request, 'rpl.html', context)
