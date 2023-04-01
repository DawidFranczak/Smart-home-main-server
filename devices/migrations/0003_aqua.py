# Generated by Django 4.1.5 on 2023-02-21 10:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("devices", "0002_delete_aqua"),
    ]

    operations = [
        migrations.CreateModel(
            name="Aqua",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("color", models.CharField(default="r255g255b255", max_length=100)),
                ("led_start", models.CharField(default="00:00:00", max_length=10)),
                ("led_stop", models.CharField(default="00:00:00", max_length=10)),
                ("fluo_start", models.CharField(default="00:00:00", max_length=10)),
                ("fluo_stop", models.CharField(default="00:00:00", max_length=10)),
                ("mode", models.BooleanField(default=False)),
                ("led_mode", models.BooleanField(default=False)),
                ("fluo_mode", models.BooleanField(default=False)),
                (
                    "sensor",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="devices.sensor"
                    ),
                ),
            ],
        ),
    ]
