import json

import requests
from django.utils.translation import gettext as _

from app.const import CHANGE_AQUA, CHECK_AQUA

from .api.serialized import AquaSerializer


def _change(message: str, sensor: object, ngrok: str, field: str) -> bool:
    """
    This function sends data to the home server for communication
    with the aquarium microcontroller for change
    RGB leds color or turn on/off leds or fluorescent lamp.

    :params message: This is a command for an aquarium microcontroller.
    :params sensor: This is an aquarium object.
    :params ngrok: This is the URL address of a home server.
    :params field: This is a field of the model to be updated.

    :return: True if the communication with aquarium is successful.
    """

    data = {"message": message, "ip": sensor.ip, "port": sensor.port}
    api = ngrok + CHANGE_AQUA

    try:
        response = requests.post(api, data=data, timeout=0.1)
        response = response.json()["response"]
    except:
        return False

    if response:
        sensor.aqua.save(update_fields=[field])

    return response


def _check(sensor: object, ngrok: str) -> bool:
    """
    This function sends aquarium settings to check the time and
    turn on/off the LEDs or fluorescent lamps depending on the time.

    :params sensor: This is an aquarium object.
    :params ngrok: This is the URL address of a home server.

    :return: True if the communication with aquarium is successful.
    """

    aqua = sensor.aqua
    settings = AquaSerializer(aqua, many=False).data
    settings["ip"] = sensor.ip
    settings["port"] = sensor.port
    api = ngrok + CHECK_AQUA

    try:
        response = requests.post(api, data=settings, timeout=1)
    except:
        return False

    response = response.json()
    success = response["response"]

    if success:
        aqua.fluo_mode = response["fluo_mode"]
        aqua.led_mode = response["led_mode"]
        aqua.save(update_fields=["fluo_mode", "led_mode"])
    return success


def change_rgb(sensor: object, ngrok: str, data: dict):
    """
    This function sends data to the home server for communication
    with the aquarium microcontroller for change
    RGB leds color or turn on/off leds or fluorescent lamp.

    :params data: This is a command for an aquarium microcontroller.
    :params sensor: This is an aquarium object.
    :params ngrok: This is the URL address of a home server.

    :return: True if change led's color is successful.
    """

    red = str(data["r"])
    green = str(data["g"])
    blue = str(data["b"])
    message = f"r{red}g{green}b{blue}"
    sensor.aqua.color = message
    return _change(message, sensor, ngrok, "color")


def change_fluo_lamp_state(sensor: object, ngrok: str, value: bool):
    """
    This function sends data to the home server for communication
    with the aquarium microcontroller for change
    fluorescent lamp mode.

    :params sensor: This is an aquarium object.
    :params ngrok: This is the URL address of a home server.
    :params value: This is a command for turn on/off fluorescent lamp(True-> ON, False-> OFF).

    :return: True if change fluorescent lamp color is successful.
    """

    message = "s1" if value else "s0"
    sensor.aqua.fluo_mode = value
    return _change(message, sensor, ngrok, "fluo_mode")


def change_led_state(sensor: object, ngrok: str, value: bool):
    """
    This function sends data to the home server for communication
    with the aquarium microcontroller for change
    led mode.

    :params sensor: This is an aquarium object.
    :params ngrok: This is the URL address of a home server.
    :params value: This is a command for turn on/off led (True-> ON, False-> OFF).

    :return: True if change led color is successful.
    """

    message = "r1" if value else "r0"
    sensor.aqua.led_mode = value
    return _change(message, sensor, ngrok, "led_mode")


def change_led_time(sensor: object, ngrok: str, data: dict):
    """
    This function sends data to the home server to check
    hours and turn on/off led depends on hours.

    :params sensor: This is an aquarium object.
    :params ngrok: This is the URL address of a home server.
    :params data: This is dictionary with LED lighting time like below

    data = {
        "led_start": "00:00:00" // hh:mm:ss
        "led_stop": "00:00:00" // hh:mm:ss
    }

    :return: True if change led time is successful and
             communication with aquarium's microcontroller is successful too.
    """

    sensor.aqua.led_start = data["led_start"]
    sensor.aqua.led_stop = data["led_stop"]
    if _check(sensor, ngrok):
        sensor.aqua.save(update_fields=["led_start", "led_stop"])
        return True
    return False


def change_fluo_lamp_time(sensor: object, ngrok: str, data: dict):
    """
    This function sends data to the home server to check
    hours and turn on/off fluorescent lamp depends on hours.

    :params sensor: This is an aquarium object.
    :params ngrok: This is the URL address of a home server.
    :params data: This is dictionary with fluorescent lamp lighting time like below

    data = {
        "fluo_lamp_start": "00:00:00" // hh:mm:ss
        "fluo_lamp_stop": "00:00:00" // hh:mm:ss
    }

    :return: True if change fluorescent lamp time is successful and
             communication with aquarium's microcontroller is successful too.
    """

    sensor.aqua.fluo_start = data["fluo_lamp_start"]
    sensor.aqua.fluo_stop = data["fluo_lamp_stop"]
    if _check(sensor, ngrok):
        sensor.aqua.save(update_fields=["fluo_start", "fluo_stop"])
        return True
    return False


def change_mode(sensor: object, ngrok: str, mode: bool):
    """
    This function sends data to the home server to check
    hours and turn on/off fluorescent lamp and led depends on hours if
    mode == True (this mean aquarium is in manual mode)

    :params sensor: This is an aquarium object.
    :params ngrok: This is the URL address of a home server.
    :params mode: This is the operating mode of the aquarium.
                  (True -> manual, False -> automatic)

    :return: True if mode is automatic and communicate with home server
    """
    sensor.aqua.mode = mode
    sensor.aqua.save(update_fields=["mode"])

    if not mode:
        return _check(sensor, ngrok)
    return False
