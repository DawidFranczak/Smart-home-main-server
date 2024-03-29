import requests
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _

from app.const import ADD_CARD, ADD_DEVICE
from devices.models import Card, Sensor, SensorSettings

user_object = object


def add_sensor(data: dict, user: user_object):
    settings = get_object_or_404(SensorSettings, fun=data["fun"])
    url = user.ngrok.ngrok + ADD_DEVICE
    sensor_port: int = settings.port
    sensor_add_message: str = settings.message
    sensor_add_response: str = settings.answer

    data = {
        "port": sensor_port,
        "message": sensor_add_message,
        "answer": sensor_add_response,
    }
    try:
        answer = requests.post(url, data=message, timeout=1).json()
    except TimeoutError:
        message = {"response": _("No communication with home server.")}
        status = 504
        return message, status

    if answer["success"]:
        if user.sensor_set.filter(ip=answer["ip"]).exists():
            return {"response": _("Sensor already exists")}, 400

        sensor = user.sensor_set.create(
            name=data["name"], fun=data["fun"], ip=answer["ip"], port=port
        )
        message = {
            "response": _("Successfully added device"),
            "id": sensor.id,
        }
        status = 201

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
        url = user.ngrok.ngrok + ADD_CARD
        data = {
            "ip": sensor.ip,
            "port": sensor.port,
        }
        try:
            answer = requests.post(url, data=data, timeout=1).json()
        except TimeoutError:
            return {"response": _("No communication with home server.")}, 504

        if answer["success"]:
            if sensor.card_set.filter(uid=answer["uid"]).exists():
                return {"response": _("This card is already exists.")}, 400

            card = sensor.card_set.create(uid=answer["uid"], name=name)
            card.save()
            return {
                "response": _("Card addes successfully."),
                "id": card.id,
            }, 201

    finally:
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

    return response, status
