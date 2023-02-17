import socket


def add_sensor(get_data, user_id):
    '''
    Comunicate and save sensor
    '''

    match get_data['fun']:
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

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for i in range(2, 254):
        check_ip = '192.168.0.'+str(i)

        try:
            sock.sendto(message, (check_ip, port))
            sock.settimeout(0.05)
            data = sock.recvfrom(128)
            response = data[0].decode('UTF-8')

            if response == answer:
                new_sensor_ip = str(data[1][0])

                if Sensor.objects.filter(ip=new_sensor_ip).exists():
                    respond = {'response': 'Czujnik już dodano'}
                    return respond

                sensor = Sensor(name=get_data['name'],
                                fun=get_data['fun'],
                                ip=new_sensor_ip,
                                user_id=user_id,
                                port=port)
                sensor.save()
                respond = {
                    'response': 'Udało sie dodać czujnik', 'id': sensor.id}
                sock.close()
                return respond

        except TimeoutError:
            continue

    else:
        respond = {'response': 'Nie udało się zapisać czujnika'}
        sock.close()
        return respond


def add_uid(_data):
    '''
        Add new rfid card to user
    '''

    respond = {}
    try:
        sensor = Sensor.objects.get(id=_data['id'])
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(('', 6721))

        except Exception as e:
            respond = {'response': 'Nie udało się otworzyć socketu'}
            return respond

        message = str.encode('add-tag')
        sock.sendto(message, (sensor.ip, sensor.port))
        sock.settimeout(9)
        data = sock.recvfrom(128)
        uid = int(data[0].decode('UTF-8'))
        sock.close()

        if Card.objects.filter(uid=uid).exists():
            respond = {'response': 'Ta karta jest już dodana'}
            return respond

        card = Card(sensor_id=sensor.id, uid=uid, name=_data['name'])
        card.save()
        respond = {'response': 'Udało sie dodać czujnik', 'id': card.id}

    except Exception as e:
        print(e)
        respond = {'response': 'Nie udało dodać się czujnika'}
        sock.close()
    return respond


# # ///////////////////////DELETE/////////////////////////////////////////
def delete_sensor(get_data):
    '''
    Delete user sensor
    '''
    # sensor_id geting from website can be 'card <number>' for rfid card
    # or '<number>' for rest of sensors

    try:
        sensor_id = str(get_data['id'])
        if sensor_id.startswith('card'):
            Card.objects.filter(id=get_data['id'].split(' ')[1]).delete()
            response = {'response': 'permission'}
            return response
        else:
            Sensor.objects.get(id=get_data['id']).delete()
            response = {'response': 'permission'}
    except:
        response = {'response': 'Nie udało się usunąć czujnika'}
    return response
