from django.utils.translation import gettext as _
from django.http import JsonResponse
import requests

from devices.models import Card, Sensor
from app.const import ADD_DEVICE, ADD_CARD


def add_sensor(data, user):

    match data['fun']:
        case 'temp':
            port = 1265
            message = str.encode('password_temp')
            answer = 'respond_temp'
        case 'sunblind':
            port = 9846
            message = str.encode('password_sunblind')
            answer = 'respond_sunblind'
        case 'light':
            port = 4324
            message = str.encode('password_light')
            answer = 'respond_light'
        case 'aqua':
            port = 7863
            message = str.encode('password_aqua')
            answer = 'respond_aqua'
        case 'stairs':
            port = 2965
            message = str.encode('password_stairs')
            answer = 'respond_stairs'
        case 'rfid':
            port = 3984
            message = str.encode('password_rfid')
            answer = 'respond_rfid'
        case 'btn':
            port = 7894
            message = str.encode('password_btn')
            answer = 'respond_btn'
        case 'lamp':
            port = 4569
            message = str.encode('password_lamp')
            answer = 'respond_lamp'

    url = user.ngrok.ngrok + ADD_DEVICE
    message = {
        "port": port,
        "message": message,
        "answer": answer,
    }
    try:
        answer = requests.post(url, data=message).json()
    except:
        message = {'response': _("No communication with home server.")}
        status = 504
        return message, status

    if answer["success"]:
        if user.sensor_set.filter(ip=answer["ip"]).exists():
            return {
                'response': _('Sensor already exists')
            }, 400

        sensor = user.sensor_set.create(name=data['name'],
                                        fun=data['fun'],
                                        ip=answer["ip"],
                                        port=port)
        message = {
            'response': _("Successfully added device"),
            'id': sensor.id,
        }
        status = 201

    message = {'response': _("System failed to add the device")}
    status = 500
    return message, status


def add_sensor_tester(get_data, request):
    EXCLUDED_SENSORS = ['temp', 'rfid', 'button', 'lamp', 'uid']

    if get_data['fun'] in EXCLUDED_SENSORS:

        message = {'response': _(
            "Sorry, you can't add this type of device in the test version")}
        status = 417

    else:
        sensor = request.user.sensor_set.create(name=get_data['name'],
                                                ip='111.111.111.111',
                                                port=1234, fun=get_data['fun'])
        message = {'response': _("Device added successfully"), 'id': sensor.id}
        status = 201

    return message, status


def add_uid(data, user):
    '''
        Add new rfid card to user
    '''
    name = data['name']

    try:
        sensor = user.sensor_set.get(id=data['id'])
        url = user.ngrok.ngrok + ADD_CARD
        data = {
            "ip": sensor.ip,
            "port": sensor.port,
        }
        try:
            answer = requests.post(url, data=data).json()
        except:
            return {
                'response': _("No communication with home server.")
            }, 504

        if answer["success"]:

            if sensor.card_set.filter(uid=answer["uid"]).exists():
                return {
                    'response': _('This card is already exists.')
                }, 400

            card = sensor.card_set.create(uid=answer["uid"], name=name)
            card.save()
            return {
                'response': _('Card addes successfully.'),
                'id': card.id,
            }, 201

    except Exception as e:
        print(e)
    finally:
        return {
            'response': _("System failed to add the device"),
        }, 500


def delete_sensor(get_data, user):
    """
    Delete user sensor
    """
    try:
        sensor_id = str(get_data['id'])
        if sensor_id.startswith('card'):
            card_id = get_data['id'].split(' ')[1]
            Card.objects.get(pk=card_id).delete()
            response = {'response': 'permission'}
            status = 200

        else:

            user.sensor_set.get(id=sensor_id).delete()
            response = {'response': 'permission'}
            status = 200

    except Sensor.DoesNotExist or Card.DoesNotExist:
        response = {'response': _("Sensor does not exists")}
        status = 404
    except:
        response = {'response': _("Failed deleted device")}
        status = 500

    return response, status
