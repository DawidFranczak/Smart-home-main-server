# Generated by Django 4.1.1 on 2023-01-05 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_homenavimage_avatar_homenavimage_home_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homenavimage',
            name='aquarium',
            field=models.ImageField(default='aqua.png', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='homenavimage',
            name='home',
            field=models.ImageField(default='home.png', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='homenavimage',
            name='light',
            field=models.ImageField(default='lamp.png', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='homenavimage',
            name='logout',
            field=models.ImageField(default='logout.png', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='homenavimage',
            name='profile',
            field=models.ImageField(default='user.png', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='homenavimage',
            name='rpl',
            field=models.ImageField(default='rfid.png', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='homenavimage',
            name='sensor',
            field=models.ImageField(default='connect.png', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='homenavimage',
            name='stairs',
            field=models.ImageField(default='stairs.png', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='homenavimage',
            name='sunblind',
            field=models.ImageField(default='sunblind.png', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='homenavimage',
            name='temperature',
            field=models.ImageField(default='temp.png', upload_to='images/'),
        ),
    ]
