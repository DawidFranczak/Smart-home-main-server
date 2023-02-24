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
        anwser = requests.put(ngrok + CHANGE_LIGHT, data=data)
        anwser = anwser.json()
        print(anwser)
        if anwser["success"]:
            light = sensor.light
            if anwser["result"] == 'ON':
                light.light = True
                response = {'response': "ON"}
            else:
                light.light = False
                response = {'response': "OFF"}
            light.save()
        else:
            response = {'response': "Nie udało się połączyć z lampą"}
    except:
        response = {'response': "Wystąpił niespodziewany błąd"}
    finally:
        return response
