# import json
import time
from datetime import datetime

from devices.models import Sensor

from .mod import check

# import requests

# from const.urls import AQUARIUM_GET_ALL, AQUARIUM_UPDATE, CLIENT_URL, SERVER_URL


def aquas_check():

    old_minutes = datetime.now().second

    while True:
        new_minutes = datetime.now().second
        if old_minutes != new_minutes:
            try:
                sensors = Sensor.objects.filter(fun="aqua")
                for sensor in sensors:
                    if not sensor.aqua.mode:
                        check(sensor, "")
                old_minutes = new_minutes
            except:
                pass
