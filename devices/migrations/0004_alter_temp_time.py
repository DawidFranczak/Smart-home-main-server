# Generated by Django 4.1.5 on 2023-03-03 15:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("devices", "0003_aqua"),
    ]

    operations = [
        migrations.AlterField(
            model_name="temp",
            name="time",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
