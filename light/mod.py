import socket


def change_light(sensor):
    '''
    communicate with lamp and try to change it state
    '''
    try:
        sock = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM)  # INTERNET / UDP
        wiad = str.encode('change')
        sock.sendto(wiad, (sensor.ip, 4324))
        sock.settimeout(1)
        data = sock.recvfrom(128)
        data = data[0].decode('UTF-8')
        light = sensor.light

        if data == 'ON':
            light.light = True
            response = {'response': 1}
        else:
            light.light = False
            response = {'response': 0}
        light.save()
    except TimeoutError:
        response = {'response': -1}
    finally:
        sock.close()
        return response
