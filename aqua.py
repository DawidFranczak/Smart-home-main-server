from datetime import datetime
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_home.settings")

django.setup()

from devices.models import Sensor
from aquarium.mod import check


def main():
    old_minutes = datetime.now().minute
    while 1:
        new_minutes = datetime.now().minute
        if old_minutes != new_minutes:
            try:
                sensors = Sensor.objects.filter(fun="aqua")
                print(sensors)
                for sensor in sensors:
                    if not sensor.aqua.mode:
                        check(sensor, "")
                old_minutes = new_minutes
            except:
                pass


if __name__ == "__main__":
    main()
