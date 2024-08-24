from datetime import datetime

from django.utils.translation import gettext as _

from app.const import CHANGE_AQUA, CHECK_AQUA
from app.UDP import send_data

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

    # data = {"message": message, "ip": sensor.ip, "port": sensor.port}
    # api = ngrok + CHANGE_AQUA

    try:
        # response = requests.post(api, data=data, timeout=0.1)
        # response = response.json()["response"]
        response = send_data(message, sensor.ip, sensor.port)
    except:
        return False

    if response:
        sensor.aqua.save(update_fields=[field])

    return response


def check(sensor: object, ngrok: str) -> bool:
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
    # api = ngrok + CHECK_AQUA

    try:
        # response = requests.post(api, data=settings, timeout=1)
        response = _check_aqua(settings)
    except:
        return False

    # response = response.json()
    success = response.get("success")

    if success:
        aqua.fluo_mode = response.get("fluo_mode")
        aqua.led_mode = response.get("led_mode")
        aqua.save(update_fields=["fluo_mode", "led_mode"])
    return success


def _check_aqua(settings: object) -> dict:
    """
    This function check time and depend on it send command
    to microcontroller about turn on/off led and fluorescent lamp

    :params request: This is incoming request from main server. In request's body
    should be dictionary like below
    {
        "led_start" : "00:00:00" // hh:mm:ss
        "led_stop" : "00:00:00" // hh:mm:ss
        "fluo_start" : "00:00:00" // hh:mm:ss
        "fluo_stop" : "00:00:00" // hh:mm:ss
        "ip" : "192.168.0.xxx" // last octet shoud be given by DHCP server
        "port" : "xxxx"
    }

    :return: If either (led and fluorescent lamp) will be check
    and communication with the microcontroller will proceed successfully
    they return dictionary like below
    {
        "response": True,
        "fluo_mode": fluo_mode, // (True -> turn on or False -> turn off)
        "led_mode": led_mode, // (True -> turn on or False -> turn off)
        "ip": ip, // microcontroller's ip
    }
    """
    led_start: str = settings.get("led_start")
    led_stop: str = settings.get("led_stop")
    fluo_start: str = settings.get("fluo_start")
    fluo_stop: str = settings.get("fluo_stop")
    ip: str = settings.get("ip")
    port: int = int(settings.get("port"))

    hour: int = datetime.now().hour
    hours: str = str(hour) if hour > 9 else "0" + str(hour)

    minute = datetime.now().minute
    minutes = str(minute) if minute > 9 else "0" + str(minute)

    time_now = "".join((hours, ":", minutes))

    if led_start < time_now < led_stop:
        led = "r1"
        led_mode = True
    else:
        led = "r0"
        led_mode = False

    if not send_data(led, ip, port):
        return {"success": False}

    if fluo_start < time_now < fluo_stop:
        fluo = "s1"
        fluo_mode = True
    else:
        fluo = "s0"
        fluo_mode = False

    if not send_data(fluo, ip, port):
        return {"success": False}
    return {
        "success": True,
        "fluo_mode": fluo_mode,
        "led_mode": led_mode,
        "ip": ip,
    }


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
    if check(sensor, ngrok):
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
    if check(sensor, ngrok):
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
        return check(sensor, ngrok)
    return False
