from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import redirect

from log.models import Ngrok
from .serialized import SensorSerializer
from .email import message
from django.core.mail import send_mail
from smart_home.settings import EMAIL_HOST_USER


@api_view(['GET'])
# /api/chart/all/
def getSensorAll(request):
    try:
        ngrok = request.GET.get('url')
        user = Ngrok.objects.get(ngrok=ngrok).user
        sensors = user.sensor_set.filter(fun='temp')
        data = [SensorSerializer(
            sensor).data for sensor in sensors]
        return Response(data)
    except Exception as e:
        print(e)
        return redirect('home')


@api_view(['PUT'])
# /api/chart/update/
def updateSensor(request):
    ngrok = request.data.get('url')
    data = request.data.get('measurment')
    user = Ngrok.objects.get(ngrok=ngrok).user
    email = []
    for measurment in data:
        if measurment['success']:
            user.sensor_set.get(ip=measurment['ip']).temp_set.create(
                temp=measurment['temp'])
        else:
            email.append(user.sensor_set.get(ip=measurment['ip']).name)
    if email:
        send_mail(
            'Błąd pomiaru temperatury',
            message(email),
            EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
        print('send email')

    return Response({"s": 's'})
