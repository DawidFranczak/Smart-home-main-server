import requests

from devices.models import Card
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
        return {
            'response': "Brak komunikacji z serwerem w domu"
        }
    if answer["success"]:
        if user.sensor_set.filter(ip=answer["ip"]).exists():
            return {
                'response': 'Czujnik już dodano'
            }

        sensor = user.sensor_set.create(name=data['name'],
                                        fun=data['fun'],
                                        ip=answer["ip"],
                                        port=port)
        return {
            'response': 'Udało sie dodać czujnik',
            'id': sensor.id,
        }
    return {
        'response': 'Nie udało sie dodać czujnik',
    }


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
                'response': "Brak komunikacji z serwerem w domu"
            }

        if answer["success"]:

            if sensor.card_set.filter(uid=answer["uid"]).exists():
                return {
                    'response': 'Ta karta jest już dodana'
                }

            card = sensor.card_set.create(uid=answer["uid"], name=name)
            card.save()
            return {
                'response': 'Udało sie dodać kartę',
                'id': card.id,
            }

    except Exception as e:
        print(e)
    finally:
        return {
            'response': 'Nie udało dodać się czujnika'
        }


def delete_sensor(get_data, user):
    """
    Delete user sensor
    """
    print(get_data)
    try:
        sensor = str(get_data['id'])
        if sensor.startswith('card'):
            card_id = get_data['id'].split(' ')[1]
            Card.objects.get(pk=card_id).delete()
            response = {'response': 'permission'}
        else:
            user.sensor_set.get(id=sensor).delete()
            response = {'response': 'permission'}
    except:
        response = {'response': 'Nie udało się usunąć czujnika'}
    return response
