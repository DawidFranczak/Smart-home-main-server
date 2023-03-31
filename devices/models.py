from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class SensorSettings(models.Model):
    fun = models.CharField(max_length=100, default="")
    message = models.CharField(max_length=100, default="")
    answer = models.CharField(max_length=100, default="")
    port = models.IntegerField()


class Sensor(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    ip = models.CharField(max_length=100)
    port = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    fun = models.CharField(max_length=100, default="")

    def __str__(self):
        return str(self.name)


class Temp(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=False)
    temp = models.FloatField()
    humi = models.FloatField(default="")

    def __str__(self):
        return str(self.sensor)


class Sunblind(models.Model):
    sensor = models.OneToOneField(Sensor, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    def __str__(self):
        return str(self.sensor)


class Aqua(models.Model):
    sensor = models.OneToOneField(Sensor, on_delete=models.CASCADE)
    color = models.CharField(max_length=100, default="r255g255b255")
    led_start = models.CharField(max_length=10, default="00:00:00")
    led_stop = models.CharField(max_length=10, default="00:00:00")
    fluo_start = models.CharField(max_length=10, default="00:00:00")
    fluo_stop = models.CharField(max_length=10, default="00:00:00")
    mode = models.BooleanField(default=False)
    led_mode = models.BooleanField(default=False)
    fluo_mode = models.BooleanField(default=False)

    def __str__(self):
        return str(self.sensor)


class Stairs(models.Model):
    sensor = models.OneToOneField(Sensor, on_delete=models.CASCADE)
    steps = models.IntegerField(default=200)
    brightness = models.IntegerField(default=100)
    lightTime = models.IntegerField(default=6)
    mode = models.BooleanField(default=False)

    def __str__(self):
        return str(self.sensor)


class Rfid(models.Model):
    sensor = models.OneToOneField(Sensor, on_delete=models.CASCADE)
    lamp = models.CharField(max_length=50, default="")

    def __str__(self):
        return str(self.sensor)


class Card(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default="")
    uid = models.IntegerField(default=0)

    def __str__(self):
        return str(self.sensor)


class Button(models.Model):
    sensor = models.OneToOneField(Sensor, on_delete=models.CASCADE)
    lamp = models.CharField(max_length=50, default="")

    def __str__(self):
        return str(self.sensor)


class Light(models.Model):
    sensor = models.OneToOneField(Sensor, on_delete=models.CASCADE)
    light = models.BooleanField(default=False)

    def __str__(self):
        return str(self.sensor)
