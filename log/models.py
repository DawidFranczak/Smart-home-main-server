from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Ngrok(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ngrok = models.URLField(default="")

    def __str__(self):
        return self.ngrok
