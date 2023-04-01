import requests
from django.utils.translation import gettext as _

from app.const import MESSAGE_SUNBLIND

ClientSerwerUrl = str

QuerySet = object


def sunblind_move(
    ngrok: ClientSerwerUrl, sensor: QuerySet, value: int
) -> tuple[str, int]:
    message = "set" + str(value)
    data = {
        "message": message,
        "ip": sensor.ip,
        "port": sensor.port,
    }
    try:
        answer = requests.put(ngrok + MESSAGE_SUNBLIND, data=data, timeout=1)

    except TimeoutError:
        message = {"message": _("No connection home server.")}
        status = 504
        return message, status

    message = {"message": _("No connection")}
    status = 504
    if answer.status_code == 200:
        sunblind = sensor.sunblind
        sunblind.value = value
        sunblind.save(updated_fiels=["value"])
        message = ""
        status = 200

    return message, status


def sunblind_move_tester(sensor: QuerySet, value: int) -> None:
    sunblind = sensor.sunblind
    sunblind.value = value
    sunblind.save(update_fields=["value"])


def sunblind_calibrations(
    ngrok: ClientSerwerUrl, sensor: QuerySet, action: str
) -> tuple[bool, int]:
    data = {
        "message": action,
        "ip": sensor.ip,
        "port": sensor.port,
    }
    try:
        answer = requests.put(ngrok + MESSAGE_SUNBLIND, data=data, timeout=1).json()
    except TimeoutError:
        answer = False
        status = 504

    # Ending calibration, set value to 100 and save in database
    if action == "end" and answer:
        sunblind = sensor.sunblind
        sunblind.value = 100
        sunblind.save(update_fields=["value"])
        status = 200

    return answer, status


def sunblind_calibrations_tester(sensor: QuerySet) -> None:
    sunblind = sensor.sunblind
    sunblind.value = 100
    sunblind.save(update_fields=["value"])
