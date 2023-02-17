import socket
from datetime import datetime


def send_data(_mess, _ip, _port):
    '''
    Send message to microcontroler on _port and _ip  and waiting for response
    '''
    try:
        wiad = str.encode(_mess)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(wiad, (_ip, _port))
        sock.settimeout(0.5)
        sock.recvfrom(128)
        sock.close()
        return True
    except:
        sock.close()
        return False


def check_aqua(sensor, aqua):
    '''
    Turn on or turn off fluo lamp and led dependence on time
    and save it to database
    '''

    if datetime.now().hour < 10:
        hours = '0' + str(datetime.now().hour)
    else:
        hours = str(datetime.now().hour)

    if datetime.now().minute < 10:
        minutes = ':0' + str(datetime.now().minute) + \
            ':' + str(datetime.now().second)
    else:
        minutes = ':' + str(datetime.now().minute) + \
            ':' + str(datetime.now().second)

    time_now = hours + minutes
    led_start = str(aqua.led_start)
    led_stop = str(aqua.led_stop)
    fluo_start = str(aqua.fluo_start)
    fluo_stop = str(aqua.fluo_stop)

    if led_start < time_now and led_stop > time_now:
        led = 'r1'
        aqua.led_mode = True
    else:
        led = 'r0'
        aqua.led_mode = False
    aqua.save()

    if not send_data(led, sensor.ip, sensor.port):
        return False

    if fluo_start < time_now and fluo_stop > time_now:
        fluo = 's1'
        aqua.fluo_mode = True
    else:
        fluo = 's0'
        aqua.fluo_mode = False
    aqua.save()

    return send_data(fluo, sensor.ip, sensor.port)
