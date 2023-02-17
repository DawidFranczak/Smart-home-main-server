# Generated by Django 4.1.5 on 2023-02-17 16:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeNavImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home', models.ImageField(default='images/home.png', upload_to='images/')),
                ('rpl', models.ImageField(default='images/rfid.png', upload_to='images/')),
                ('aquarium', models.ImageField(default='images/aqua.png', upload_to='images/')),
                ('sunblind', models.ImageField(default='images/sunblind.png', upload_to='images/')),
                ('temperature', models.ImageField(default='images/temp.png', upload_to='images/')),
                ('profile', models.ImageField(default='images/user.png', upload_to='images/')),
                ('light', models.ImageField(default='images/lamp.png', upload_to='images/')),
                ('stairs', models.ImageField(default='images/stairs.png', upload_to='images/')),
                ('sensor', models.ImageField(default='images/sensor.png', upload_to='images/')),
                ('logout', models.ImageField(default='images/logout.png', upload_to='images/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]