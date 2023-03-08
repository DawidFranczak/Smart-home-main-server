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
            return {'response': _("No nconnection home server.")}

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
            return response
        else:
            return {'response': _("No nconnection with lamp")}
    except:
        return {'response': _("Unexpected error")}
