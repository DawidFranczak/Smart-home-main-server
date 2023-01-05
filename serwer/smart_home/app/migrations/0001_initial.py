# Generated by Django 4.1.1 on 2023-01-03 18:01

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('avatar', models.ImageField(default='user.png', upload_to='')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('ip', models.CharField(max_length=100)),
                ('port', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('fun', models.CharField(default='', max_length=100)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Temp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('temp', models.CharField(max_length=10)),
                ('humi', models.CharField(default='', max_length=10)),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.sensor')),
            ],
        ),
        migrations.CreateModel(
            name='Sunblind',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.sensor')),
            ],
        ),
        migrations.CreateModel(
            name='Stairs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('steps', models.IntegerField(default=200)),
                ('brightness', models.IntegerField(default=100)),
                ('lightTime', models.IntegerField(default=6)),
                ('mode', models.BooleanField(default=False)),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.sensor')),
            ],
        ),
        migrations.CreateModel(
            name='Rfid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lamp', models.CharField(default='', max_length=50)),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.sensor')),
            ],
        ),
        migrations.CreateModel(
            name='Light',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('light', models.BooleanField()),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.sensor')),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('uid', models.IntegerField(default=0)),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.sensor')),
            ],
        ),
        migrations.CreateModel(
            name='Button',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lamp', models.CharField(default='', max_length=50)),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.sensor')),
            ],
        ),
        migrations.CreateModel(
            name='Aqua',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(default='', max_length=100)),
                ('led_start', models.CharField(default='00:00:00', max_length=10)),
                ('led_stop', models.CharField(default='00:00:00', max_length=10)),
                ('fluo_start', models.CharField(default='00:00:00', max_length=10)),
                ('fluo_stop', models.CharField(default='00:00:00', max_length=10)),
                ('mode', models.BooleanField(default=False)),
                ('led_mode', models.BooleanField(default=False)),
                ('fluo_mode', models.BooleanField(default=False)),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.sensor')),
            ],
        ),
    ]
