# Generated by Django 4.1.1 on 2022-09-24 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_aqua_fluo_start_aqua_fluo_stop_aqua_led_start_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='aqua',
            name='fluo_mode',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='aqua',
            name='led_mode',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='aqua',
            name='color',
            field=models.CharField(default='', max_length=100),
        ),
    ]
