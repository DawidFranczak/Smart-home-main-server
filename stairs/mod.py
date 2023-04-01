import requests
from django.http import JsonResponse
from django.utils.translation import gettext as _

from app.const import CHANGE_STAIRS


def stairs_settings(get_data, sensor, stairs, ngrok):
    match get_data["action"]:
        case "set-lightingTime":
            stairs.lightTime = int(get_data["lightingTime"])
            message = "te" + str(get_data["lightingTime"])
            field = "lightTime"

        case "set-brightness":
            stairs.brightness = int(get_data["brightness"])
            message = "bs" + str(get_data["brightness"])
            field = "brightness"

        case "set-step":
            stairs.steps = int(get_data["step"])
            message = "sp" + str(get_data["step"])
            field = "steps"

        case "change-stairs":
            field = "mode"

            if stairs.mode:
                stairs.mode = False
                message = "OFF"
            else:
                stairs.mode = True
                message = "ON"

    # Control simulation
    if sensor.name == "tester":
        stairs.save(update_fields=[field])
        message = {"respond": _("Settings updated successfully")}
        status = 200
        return message, status
    # End simulation

    data = {
        "message": message,
        "ip": sensor.ip,
        "port": sensor.port,
    }
    try:
        answer = requests.put(ngrok + CHANGE_STAIRS, data=data).json()
    except:
        message = {"respond": _("No connection with home server.")}
        status = 504
        return message, status

    message = {"respond": _("No connection with stairs")}
    status = 500

    if answer:
        stairs.save(update_fields=[field])
        message = {"respond": _("Settings updated successfully")}
        status = 200

    return message, status
