from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
import json

# Create your views here.


class RplView(View):
    template_name = 'rpl.html'

    def get(self, request):
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

        return render(request, self.template_name, context)

    def post(self, request):

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

            # RFID
            sensors_rfid = request.user.sensor_set.filter(
                fun='rfid')
            connected_rfid = set([
                sensor.id for sensor in sensors_rfid if sensor.rfid.lamp == lamp.ip])
            add_rfids = set([int(rfid_id) for rfid_id in get_data['rfids']])

            connect_rfid = add_rfids - connected_rfid
            remove_rfid = connected_rfid - add_rfids

            # Buttons
            sensor_buttons = request.user.sensor_set.filter(
                fun='btn')
            connected_buttons = set([
                sensor.id for sensor in sensor_buttons if sensor.button.lamp == lamp.ip])
            add_buttons = set([int(button_id)
                              for button_id in get_data['btns']])

            connect_buttons = add_buttons - connected_buttons
            remove_buttons = connected_buttons - add_buttons

            for id in connect_rfid:
                rfid = request.user.sensor_set.get(pk=id).rfid
                rfid.lamp = lamp.ip
                rfid.save()

            for id in remove_rfid:
                rfid = request.user.sensor_set.get(pk=id).rfid
                rfid.lamp = ""
                rfid.save()

            for id in connect_buttons:
                btn = request.user.sensor_set.get(pk=id).button
                btn.lamp = lamp.ip
                btn.save()

            for id in remove_buttons:
                btn = request.user.sensor_set.get(pk=id).button
                btn.lamp = ""
                btn.save()

            message = {'message': 'Połączono'}
            return JsonResponse(message)
