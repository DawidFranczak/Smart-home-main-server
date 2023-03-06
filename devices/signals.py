<<<<<<< HEAD:app/signals.py
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from user_page.models import HomeNavImage
from random import randint
from datetime import datetime, timedelta
from django.db.models import Q


def tester_chart_data(user):
    """
        Additions random temperature measurment to one tester device
    """

    sensor = user.device_set.get(
        Q(user_id=user.id) &
        Q(fun='temp') &
        Q(name='tester'))

    data_from = str(datetime.now().date() - timedelta(days=9)).split('-')
    month = int(data_from[1])
    day = int(data_from[2])
    miesiac = month
    dzien = day
    godzina = 0

    for i in range(10):
        for i in range(24):
            try:
                y = datetime(2023, miesiac, dzien, godzina, 0, 0)
            except ValueError:
                dzien = 1
                miesiac += 1
                godzina = 0
            x = randint(0, 20)
            yy = randint(0, 100)
            sensor.temp_set.create(
                sensor_id=sensor.id, time=y, temp=x, humi=yy)
            godzina += 1

        godzina = 0
        dzien += 1


def add_sensors_to_tester(user):
    """
        Adding few sensor to tester user
    """
    ip = 100
    FUNCTION = ['temp', 'sunblind', 'light',
                'aqua', 'stairs', 'rfid', 'btn', 'lamp']
    NAME = ['', 'bardzo długa i nieciekawa nazwa ',
            'bardzo długa i nieciekawa nazwa tylko że druga ']
    for fun in FUNCTION:
        for name in NAME:
            user.device_set.create(
                user=user, name=name+'tester', ip='111.111.111.'+str(ip), port=1111, fun=fun)
            ip += 1
    for sensor in user.device_set.filter(fun='rfid'):
        for name in NAME:
            sensor.card_set.create(name=name + 'tester',
                                   uid=11111111)

    tester_chart_data(user)


@receiver(post_save, sender=User)
def create_home_nav_image(sender, instance, created, **kwarg):
    if created:
        HomeNavImage.objects.create(user=instance)
        if 'tester' in instance.username:
            add_sensors_to_tester(instance)
=======
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.dispatch import receiver
from django.db.models import Q
import threading

from user_page.models import HomeNavImage
from log.models import Ngrok
from random import randint
import time
from .models import *


def tester_chart_data(user):
    """
        Additions random temperature measurment to one tester sensor
    """

    sensor = Sensor.objects.get(
        Q(user_id=user.id) &
        Q(fun='temp') &
        Q(name='tester'))

    data_from = str(datetime.now().date() - timedelta(days=8)).split('-')
    month = int(data_from[1])
    day = int(data_from[2])
    # month = 1
    # day = 1
    hour = 0
    year = 2023
    # for i in range(50):
    for j in range(8):
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


def add_sensors_to_tester(user):
    """
        Adding few sensor to tester user
    """
    start = time.time()
    print("Start")
    ip = 100
    FUNCTION = ['temp', 'sunblind', 'light',
                'aqua', 'stairs', 'rfid', 'btn', 'lamp']

    NAME = ['', 'bardzo długa i nieciekawa nazwa ',
            'bardzo długa i nieciekawa nazwa tylko że druga ']

    for fun in FUNCTION:
        for name in NAME:
            Sensor.objects.create(
                user=user, name=name+'tester', ip='111.111.111.'+str(ip), port=1111, fun=fun)
            ip += 1
    for sensor in Sensor.objects.filter(user=user, fun='rfid'):
        for name in NAME:
            Card.objects.create(sensor=sensor, name=name +
                                'tester', uid=11111111)

    tester_chart_data(user)
    print(f"time: {time.time()-start}")


@receiver(post_save, sender=User)
def create_home_nav_image(sender, instance, created, **kwarg):
    if created:
        HomeNavImage.objects.create(user=instance)
        Ngrok.objects.create(user=instance)

        if 'tester' in instance.username:
            temp = threading.Thread(target=add_sensors_to_tester,
                                    args=[instance])
            temp.start()

            # add_sensors_to_tester(instance)


@receiver(post_save, sender=Sensor)
def add_sensor(sender, instance, created, **kwarg):
    if created:
        function = instance.fun
        match function:
            case 'sunblind':
                Sunblind.objects.create(sensor_id=instance.id)

            case 'light':
                Light.objects.create(sensor_id=instance.id)

            case 'stairs':
                Stairs.objects.create(sensor_id=instance.id)

            case 'rfid':
                Rfid.objects.create(sensor_id=instance.id)

            case 'btn':
                Button.objects.create(sensor_id=instance.id)

            case 'aqua':
                Aqua.objects.create(sensor_id=instance.id)
>>>>>>> translate:devices/signals.py
