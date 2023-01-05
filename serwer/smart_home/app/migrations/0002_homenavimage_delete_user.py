# Generated by Django 4.1.1 on 2023-01-04 14:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeNavImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(default='user.png', upload_to='static/images')),
                ('rpl', models.ImageField(default='rfid.png', upload_to='static/images')),
                ('aquarium', models.ImageField(default='aqua.png', upload_to='static/images')),
                ('sunblind', models.ImageField(default='sunblind.png', upload_to='static/images')),
                ('temperature', models.ImageField(default='temp.png', upload_to='static/images')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
