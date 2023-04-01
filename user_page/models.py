from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class HomeNavImage(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    home = models.ImageField(upload_to="images/", default="images/home.png")
    rpl = models.ImageField(upload_to="images/", default="images/rfid.png")
    aquarium = models.ImageField(upload_to="images/", default="images/aqua.png")
    sunblind = models.ImageField(upload_to="images/", default="images/sunblind.png")
    temperature = models.ImageField(upload_to="images/", default="images/temp.png")
    profile = models.ImageField(upload_to="images/", default="images/user.png")
    light = models.ImageField(upload_to="images/", default="images/lamp.png")
    stairs = models.ImageField(upload_to="images/", default="images/stairs.png")
    sensor = models.ImageField(upload_to="images/", default="images/sensor.png")
    logout = models.ImageField(upload_to="images/", default="images/logout.png")

    def __str__(self):
        return str(self.user)
