from django.utils.translation import gettext as _
import requests

from app.const import CHANGE_LIGHT


def change_light(sensor, ngrok):
    """
    Communicate with lamp and try to change it state
"""
    try:
        data = {
            "ip": sensor.ip,
            "port": sensor.port,
        }
        try:
            answer = requests.put(ngrok + CHANGE_LIGHT, data=data)
        except:
            return {'response': _("No nconnection home server.")}, 200

        answer = answer.json()
        if answer["success"]:
            light = sensor.light
            if answer["result"] == 'ON':
                light.light = True
                response = {'response': "ON"}
            else:
                light.light = False
                response = {'response': "OFF"}
            light.save(update_fields=["light"])
            return response, 200
        else:
            return {'response': _("No connection with lamp")}, 500
    except:
        return {'response': _("Unexpected error")}, 500
