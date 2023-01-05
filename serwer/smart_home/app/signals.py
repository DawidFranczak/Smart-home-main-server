from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import HomeNavImage

@receiver(post_save, sender = User)
def create_home_nav_image(sender, instance, created, **kwarg):
    if created:
        HomeNavImage.objects.create(user = instance)