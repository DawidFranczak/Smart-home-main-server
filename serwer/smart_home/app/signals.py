from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import *

@receiver(post_save, sender = User)
def create_home_nav_image(sender, instance, created, **kwarg):
    if created:
        HomeNavImage.objects.create(user = instance)
        
@receiver(post_save, sender = Sensor)
def add_sensor(sender, instance, created,**kwarg):
    if created:
        function = instance.fun
        match function:
            case 'sunblind':
                Sunblind.objects.create(sensor_id = instance.id)

            case 'light':
                Light.objects.create(sensor_id = instance.id)

            case 'aqua':
                Aqua.objects.create(sensor_id = instance.id)
                        
            case 'stairs':
                Stairs.objects.create(sensor_id = instance.id)
                
            case 'rfid':
                Rfid.objects.create(sensor_id = instance.id)
                           
            case 'btn':
                Button.objects.create(sensor_id = instance.id)
                           
            
