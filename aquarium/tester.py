import json
from datetime import datetime

from django.utils.translation import gettext as _


def _check_aqua_testet(aqua: object) -> None:
    led_start = aqua.led_start
    led_stop = aqua.led_stop
    fluo_start = aqua.fluo_start
    fluo_stop = aqua.fluo_stop

    hour: int = datetime.now().hour
    hours: str = str(hour) if hour > 9 else "0" + str(hour)

    minute = datetime.now().minute
    minutes = str(minute) if minute > 9 else "0" + str(minute)

    time_now = hours + minutes

    led_mode = True if led_start < time_now < led_stop else False

    fluo_mode = True if fluo_start < time_now < fluo_stop else False
    aqua.fluo_mode = fluo_mode
    aqua.led_mode = led_mode
    aqua.save(update_fields=["fluo_mode", "led_mode"])


def aquarium_contorler_tester(request, aqua: object) -> None:
    """
    This function changes the aquarium settings without communicating with the home server.
    This means that the operation performed below is always successful.
    This function is only for demonstrating the website's functionality and will be removed in the near future.
    """

    get_data = json.loads(request.body)
    match get_data["action"]:
        case "changeRGB":
            red = str(get_data["r"])
            green = str(get_data["g"])
            blue = str(get_data["b"])
            message = f"r{red}g{green}b{blue}"
            aqua.color = message
            aqua.save(update_fields=["color"])

        case "changeFluoLampState":
            aqua.fluo_mode = get_data["value"]
            aqua.save(update_fields=["fluo_mode"])

        case "changeLedState":
            aqua.led_mode = get_data["value"]
            aqua.save(update_fields=["led_mode"])

        case "changeLedTime":
            aqua.led_start = get_data["ledStart"]
            aqua.led_stop = get_data["ledStop"]
            _check_aqua_testet(aqua)
            aqua.save(update_fields=["led_start", "led_stop"])

        case "changeFluoLampTime":
            aqua.fluo_start = get_data["fluoLampStart"]
            aqua.fluo_stop = get_data["fluoLampStop"]
            _check_aqua_testet(aqua)
            aqua.save(update_fields=["fluo_start", "fluo_stop"])

        case "changeMode":
            aqua.mode = get_data["mode"]
            aqua.save(update_fields=["mode"])

            if get_data["mode"]:
                response = {"fluo": aqua.fluo_mode, "led": aqua.led_mode}
                return response
            _check_aqua_testet(aqua)
