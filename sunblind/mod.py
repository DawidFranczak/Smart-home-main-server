from django.utils.translation import gettext as _
import requests

from app.const import MESSAGE_SUNBLIND


def sunblind_move(ngrok, sensor, get_data):
    message = 'set' + str(get_data['value'])
    data = {
        "message": message,
        "ip": sensor.ip,
        "port": sensor.port,
    }
    try:
        answer = requests.put(ngrok + MESSAGE_SUNBLIND, data=data)

    except:
        message = {
            'message': _("No connection home server.")
        }
        status = 504
        return message, status

    message = {'message': _('No connection')}
    status = 504
    if answer.status_code == 200:
        sunblind = sensor.sunblind
        sunblind.value = get_data['value']
        sunblind.save(updated_fiels=["value"])
        message = ""
        status = 200

    return message, status


def sunblind_move_tester(sensor, get_data) -> None:
    sunblind = sensor.sunblind
    sunblind.value = get_data['value']
    sunblind.save(update_fields=["value"])


def sunblind_calibrations(ngrok, sensor, get_data):
    data = {
        "message": get_data['action'],
        "ip": sensor.ip,
        "port": sensor.port,
    }
    try:
        answer = requests.put(ngrok + MESSAGE_SUNBLIND, data=data).json()
    except:
        answer = False
        status = 504

    # Ending calibration, set value to 100 and save in database
    if get_data['action'] == 'end' and answer:

        sunblind = sensor.sunblind
        sunblind.value = 100
        sunblind.save(update_fields=["value"])
        status = 200

    return answer, status


def sunblind_calibrations_tester(sensor) -> None:
    sunblind = sensor.sunblind
    sunblind.value = 100
    sunblind.save(update_fields=["value"])
