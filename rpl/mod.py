import requests
from django.core.exceptions import ObjectDoesNotExist

from app.UDP import send_data
from devices.models import Sensor

# from const.urls import CLIENT_URL, LAMP_CHECK, SERVER_URL, UID_CHECK


def check_uid(uid, ip, port) -> None:
    """
    This function sends the UID of a card to the main server and waits for
    a response.Depending on the server's answer, it will send a command to
    open or not open the gate.

    :params uid:
    :params ip:
    :params port:
    """

    # data: dict = {
    #     "uid": uid,
    #     "ip": ip,
    #     "url": CLIENT_URL,
    # }
    # answer = requests.post(SERVER_URL + UID_CHECK, data=data, timeout=1).json()
    try:
        user = Sensor.objects.get(ip=ip).user
        if not user:
            send_data("acces-denied", ip, port)
            return

        card = user.sensor_set.get(ip=ip).card_set.filter(uid=uid)
        access = card.exists()
    except ObjectDoesNotExist:
        access = False

    finally:
        mess = "access" if access else "acces-denied"
        send_data(mess, ip, port)


def check_lamp(message, ip) -> None:
    """
    This function sends microcontroller's ip to the main server
    and get lamp's microcontroller ip and port connected with first microcontroller
    (rpl side on webside)

    :params message: This is message whith shoud be sends to lamp's microcontroller
    :params ip: This is ip address microcontroller
    """

    # data: dict = {
    #     "ip": ip,
    #     "url": CLIENT_URL,
    # }
    # answer = requests.post(SERVER_URL + LAMP_CHECK, data=data, timeout=1).json()

    try:
        user = Sensor.objects.get(ip=ip).user
        sensor_lamp_ip = user.sensor_set.get(ip=ip).rfid.lamp
        lamp = user.sensor_set.get(ip=sensor_lamp_ip)

    except ObjectDoesNotExist:
        return {"success": False}

    finally:
        send_data(message, lamp.ip, lamp.port)
