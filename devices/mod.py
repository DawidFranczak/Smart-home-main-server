import socket

import requests
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _

from app.const import ADD_CARD, ADD_DEVICE
from devices.models import Card, Sensor, SensorSettings

user_object = object


def add_sensor(data: dict, user: user_object):
    settings = get_object_or_404(SensorSettings, fun=data["fun"])
    # url = user.ngrok.ngrok + ADD_DEVICE
    sensor_port: int = settings.port
    sensor_add_message: str = settings.message
    sensor_add_response: str = settings.answer

    # data = {
    #     "port": sensor_port,
    #     "message": sensor_add_message,
    #     "answer": sensor_add_response,
    # }
    # try:
    answer = _add_device(sensor_add_message, sensor_add_response, sensor_port)
    # except TimeoutError:
    #     message = {"response": _("No communication with home server.")}
    #     status = 504
    #     return message, status

    if answer.get("success"):
        if user.sensor_set.filter(ip=answer.get("ip")).exists():
            return {"response": _("Sensor already exists")}, 400

        sensor = user.sensor_set.create(
            name=data["name"], fun=data["fun"], ip=answer["ip"], port=sensor_port
        )
        message = {
            "response": _("Successfully added device"),
            "id": sensor.id,
        }
        status = 201
    else:
        message = {"response": _("System failed to add the device")}
        status = 500
    return message, status


def add_sensor_tester(get_data: dict, request: object):
    EXCLUDED_SENSORS = ["temp", "rfid", "button", "lamp", "uid"]

    if get_data["fun"] in EXCLUDED_SENSORS:
        message = {
            "response": _(
                "Sorry, you can't add this type of device in the test version"
            )
        }
        status = 417

    else:
        sensor = request.user.sensor_set.create(
            name=get_data["name"], ip="111.111.111.111", port=1234, fun=get_data["fun"]
        )
        message = {"response": _("Device added successfully"), "id": sensor.id}
        status = 201

    return message, status


def add_uid(data: dict, user: user_object):
    """
    Add new rfid card to user
    """
    name = data["name"]

    try:
        sensor = user.sensor_set.get(id=data["id"])
        # url = user.ngrok.ngrok + ADD_CARD
        # data = {
        #     "ip": sensor.ip,
        #     "port": sensor.port,
        # }
        # try:
        # answer = requests.post(url, data=data, timeout=1).json()
        # except TimeoutError:
        # return {"response": _("No communication with home server.")}, 504
        answer = _add_card(sensor.ip, sensor.port)
        print(answer)
        if answer.get("success"):
            if sensor.card_set.filter(uid=answer.get("uid")).exists():
                return {"response": _("This card is already exists.")}, 400

            card = sensor.card_set.create(uid=answer.get("uid"), name=name)
            card.save()
            return {
                "response": _("Card addes successfully."),
                "id": card.id,
            }, 201

    except:
        return {
            "response": _("System failed to add the device"),
        }, 500


def delete_sensor(get_data: dict, user: user_object):
    """
    Delete user sensor
    """
    try:
        sensor_id = str(get_data["id"])
        if sensor_id.startswith("card"):
            card_id = get_data["id"].split(" ")[1]
            Card.objects.get(pk=card_id).delete()
            response = {"response": "permission"}
            status = 200

        else:
            user.sensor_set.get(id=sensor_id).delete()

            response = {"response": "permission"}
            status = 200

    except Sensor.DoesNotExist or Card.DoesNotExist:
        response = {"response": _("Sensor does not exists")}
        status = 404
    except:
        response = {"response": _("Failed deleted device")}
        status = 500

    return (response,)


def _add_device(message: str, answer: str, port: int) -> dict:
    """
    This function searches the local network for microcontroller with
    a specific IP address range (192.168.0.2 - 192.168.0.253) and specific port.

    :params message: This is message for microcontroller (they shoud be a password)
    :params answer: This is answer from microcontroller on our message.
    :params port: This is the port under which the IP addresses will be scanned

    :return:If the microcontroller is found and its response is correct,
    the function will return a dictionary like below
    {
        "success": True,
        "ip": new_sensor_ip,
    }
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for i in range(2, 254):
        check_ip = "192.168.1." + str(i)
        print(check_ip)
        try:
            sock.sendto(bytes(message, "utf-8"), (check_ip, port))
            sock.settimeout(0.05)
            data = sock.recvfrom(128)
            response = data[0].decode("UTF-8")
            if response == answer:
                new_sensor_ip = str(data[1][0])
                sock.close()

                return {
                    "success": True,
                    "ip": new_sensor_ip,
                }

        except:
            continue

    sock.close()
    return {
        "success": False,
    }


def _add_card(ip: str, port: int) -> dict:
    """
    This function sends a command to the RFID sensor
    to add a new card and waits for a new UID.

    :params ip: This is the IP address of the RFID sensor
    :params port: This is the port of the RFID sensor

    :return: If uid read successfully return dictionary like below
    {
        "success": True,
        "uid": uid
    }
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:

        sock.sendto(str.encode("add-tag"), (ip, port))
        sock.settimeout(10)
    except TimeoutError:
        sock.close()
        return {"success": False}

    data = sock.recvfrom(128)
    uid = int(data[0].decode("UTF-8"))
    return {"success": True, "uid": uid}
