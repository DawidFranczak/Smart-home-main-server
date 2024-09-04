import threading
import time
from datetime import datetime, timedelta
from random import randint

from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from log.models import Ngrok
from user_page.models import HomeNavImage

from .models import *


def tester_chart_data(user: object) -> None:
    """
    Additions random temperature measurment to one tester sensor
    """

    sensor = Sensor.objects.get(Q(user_id=user.id) & Q(fun="temp") & Q(name="tester"))

    data_from = str(datetime.now().date() - timedelta(days=8)).split("-")
    month = int(data_from[1])
    day = int(data_from[2])
    # month = 1
    # day = 1
    hour = 0
    year = 2024
    # for i in range(50):
    for j in range(9):
        for k in range(24):
            try:
                y = datetime(year, month, day, hour, 0, 0)
            except ValueError:
                if month > 12:
                    year += 1
                    month = 0
                    print(year)
                day = 1
                month += 1
                hour = 0

            x = randint(0, 20)
            yy = randint(0, 100)
            p = Temp(sensor_id=sensor.id, time=y, temp=x, humi=yy)
            p.save()
            hour += 1

        hour = 0
        day += 1


def add_sensors_to_tester(user: object) -> None:
    """
    Adding few sensor to tester user
    """
    start = time.time()
    print("Start")
    ip = 100
    FUNCTION = ["temp", "sunblind", "light", "aqua", "stairs", "rfid", "btn", "lamp"]

    NAME = [
        "",
        "bardzo długa i nieciekawa nazwa ",
        "bardzo długa i nieciekawa nazwa tylko że druga ",
    ]

    for fun in FUNCTION:
        for name in NAME:
            Sensor.objects.create(
                user=user,
                name=name + "tester",
                ip="111.111.111." + str(ip),
                port=1111,
                fun=fun,
            )
            ip += 1
    for sensor in Sensor.objects.filter(user=user, fun="rfid"):
        for name in NAME:
            Card.objects.create(sensor=sensor, name=name + "tester", uid=11111111)

    tester_chart_data(user)
    print(f"time: {time.time()-start}")


@receiver(post_save, sender=User)
def create_home_nav_image(sender, instance, created, **kwarg) -> None:
    if created:
        HomeNavImage.objects.create(user=instance)
        Ngrok.objects.create(user=instance)

        if "tester" in instance.username:
            temp = threading.Thread(target=add_sensors_to_tester, args=[instance])
            temp.start()


@receiver(post_save, sender=Sensor)
def add_sensor(sender, instance, created, **kwarg) -> None:
    if created:
        function = instance.fun
        match function:
            case "sunblind":
                Sunblind.objects.create(sensor_id=instance.id)

            case "light":
                Light.objects.create(sensor_id=instance.id)

            case "stairs":
                Stairs.objects.create(sensor_id=instance.id)

            case "rfid":
                Rfid.objects.create(sensor_id=instance.id)

            case "btn":
                Button.objects.create(sensor_id=instance.id)

            case "aqua":
                Aqua.objects.create(sensor_id=instance.id)


@receiver(post_migrate)
def add_default_values(sender, **kwargs):
    if not SensorSettings.objects.filter(fun="aqua").exists():
        SensorSettings.objects.create(
            fun="aqua", message="password_aqua", answer="respond_aqua", port=7863
        )
    # if not SensorSettings.objects.filter(fun="sunblind").exists():
    #     SensorSettings.objects.create(
    #         fun="sunblind", message="", answer="", port=
    #     )
    # if not SensorSettings.objects.filter(fun="temp").exists():
    #     SensorSettings.objects.create(
    #         fun="temp", message="", answer="", port=
    #     )
    # if not SensorSettings.objects.filter(fun="light").exists():
    #     SensorSettings.objects.create(
    #         fun="light", message="", answer="", port=
    #     )
    # if not SensorSettings.objects.filter(fun="stairs").exists():
    #     SensorSettings.objects.create(
    #         fun="stairs", message="", answer="", port=
    #     )
    if not SensorSettings.objects.filter(fun="rfid").exists():
        SensorSettings.objects.create(
            fun="rfid", message="password_rfid", answer="respond_rfid", port=3984
        )
    if not SensorSettings.objects.filter(fun="btn").exists():
        SensorSettings.objects.create(
            fun="button", message="password_btn", answer="respond_btn", port=7894
        )
    if not SensorSettings.objects.filter(fun="lamp").exists():
        SensorSettings.objects.create(
            fun="lamp", message="password_lamp", answer="respond_lamp", port=4569
        )
    # if not SensorSettings.objects.filter(fun="uid").exists():
    #     SensorSettings.objects.create(
    #         fun="uid", message="", answer="", port=
    #     )
    # if not SensorSettings.objects.filter(fun="").exists():
    #     SensorSettings.objects.create(
    #         fun="", message="", answer="", port=
    #     )
