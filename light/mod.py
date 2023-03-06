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
            return {'response': "Brak komunikacji z serwerem w domu"}

        answer = answer.json()
        if answer["success"]:
            light = sensor.light
            if answer["result"] == 'ON':
                light.light = True
                response = {'response': "ON"}
            else:
                light.light = False
                response = {'response': "OFF"}
            light.save()
        else:
            return {'response': "Nie udało się połączyć z lampą"}
    except:
        return {'response': "Wystąpił niespodziewany błąd"}
