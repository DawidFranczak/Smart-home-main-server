# Generated by Django 4.1.1 on 2023-01-05 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_homenavimage_aquarium_alter_homenavimage_home_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homenavimage',
            name='aquarium',
            field=models.ImageField(default='images/aqua.png', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='homenavimage',
            name='home',
            field=models.ImageField(default='images/home.png', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='homenavimage',
            name='light',
            field=models.ImageField(default='images/lamp.png', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='homenavimage',
            name='logout',
            field=models.ImageField(default='images/logout.png', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='homenavimage',
            name='profile',
            field=models.ImageField(default='images/user.png', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='homenavimage',
            name='rpl',
            field=models.ImageField(default='images/rfid.png', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='homenavimage',
            name='sensor',
            field=models.ImageField(default='images/connect.png', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='homenavimage',
            name='stairs',
            field=models.ImageField(default='images/stairs.png', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='homenavimage',
            name='sunblind',
            field=models.ImageField(default='images/sunblind.png', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='homenavimage',
            name='temperature',
            field=models.ImageField(default='images/temp.png', upload_to='images/'),
        ),
    ]