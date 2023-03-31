from datetime import datetime


def check_aqua_testet(aqua: object) -> bool:
    """
    Turn on or turn off fluo lamp and led dependence on time
    and save it to database
    """

    led_start = aqua.led_start
    led_stop = aqua.led_stop
    fluo_start = aqua.fluo_start
    fluo_stop = aqua.fluo_stop

    hour: int = datetime.now().hour
    hours: str = str(hour) if hour > 9 else "0" + hour

    minute = datetime.now().minute
    minutes = str(minute) if minutes > 9 else "0" + minutes

    time_now = hours + minutes

    led_mode = True if led_start < time_now < led_stop else False

    fluo_mode = True if fluo_start < time_now < fluo_stop else False

    aqua.fluo_mode = fluo_mode
    aqua.led_mode = led_mode
    aqua.save(update_fields=["fluo_mode", "led_mode"])
    return True
