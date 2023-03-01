from datetime import datetime


def check_aqua_testet(aqua):
    '''
    Turn on or turn off fluo lamp and led dependence on time
    and save it to database
    '''

    led_start = aqua.led_start
    led_stop = aqua.led_stop
    fluo_start = aqua.fluo_start
    fluo_stop = aqua.fluo_stop

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

    led_mode = True if led_start < time_now and led_stop > time_now else False

    fluo_mode = True if fluo_start < time_now and fluo_stop > time_now else False

    aqua.fluo_mode = fluo_mode
    aqua.led_mode = led_mode
    aqua.save()
    return True
