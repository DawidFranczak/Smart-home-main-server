from email.errors import MessageParseError
from inspect import Attribute
from multiprocessing import context
from string import capwords
from urllib import request
from urllib.request import Request
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from datetime import datetime, timedelta

from .forms import CreateUserForm


from speaker import check_aqua_all
from .models import *
import socket
from .mod import *
import json

from time import sleep
from random import randint

# Create your views here.

def registerUser(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            form.save()  
            messages.success(request,'Rejestracja przebiegła pomyślnie.')
            return redirect('login') 
        
    context = {'form': form}
    return render(request, 'base/register.html',context)


def loginUser(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == "" or password == "":
            messages.error(request, 'Proszę wypełnić obydwa pola.')
            return redirect('login')
        
        if  User.objects.filter(username=username).exists():
            user = authenticate(request, username=username, password=password)
        else:
            messages.error(request, 'Użytkownik nie istenieje.')
            return redirect('login')
        
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Nazwa albo hasło są nieprawidłowe.')
            return redirect('login')
        
    return render(request, 'base/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    # if request.method == 'POST':
    #     login = request.form['login"]
    #     haslo = request.form["haslo"]
    # context = {}
    # s = Temp(sensor_id=Sensor.objects.get(name = 'room').id ,temp = '11', humi = '122')
    # s.save()
    # sensor = Sensor.objects.all()
    # sensor = Sensor.objects.get(name = 'room').id

    # context = {'sensor': sensor}
    
    # miesiac = 1
    # dzien = 1
    # godzina = 0
    # iddd = 1
    # for i in range(12):
    #     while(dzien != 32):
    #         try:
    #             y = datetime(2022,miesiac,dzien,godzina,0,0)
    #             # print(y)
    #         except ValueError:
    #             dzien = 1
    #             miesiac += 1
    #             godzina = 0
    #         x = randint(0,20)
    #         yy = randint(0,100)
    #         iddd += 1
    #         pomiar = [(iddd, y, x, y,74)]
    #         p = Temp(sensor_id = 74,time = y, temp = x , humi = yy )
    #         p.save()
    #         print(pomiar)
    #         godzina += 1
    #         if (godzina == 24):
    #             godzina = 0
    #             dzien += 1
    #         sleep(0.01)
    #     dzien = 1
    #     miesiac += 1
    
    # tem = [5.6,5.7,5.9,5.6,5.1,4.5,4.4,5.7,7.7,8.5,9.9,10.8,11.2,10.8,9.9,8.8,8.4,7.9,8.2,8.0,8.0,8.3,8.4,7.9,7.6,7.6,7.7,7.7,7.5,7.2,7.3,7.2,7.2,7.5,8.1,8.9,9.4,8.8,7.7,6.3,5.7,5.1,4.8,4.8,5.2,5.9,6.9,8.1,9.4,10.0,10.3,10.6,10.6,10.5,10.5,10.9,11.4,12.0,12.4,12.7,12.9,12.9,12.6,12.5,12.6,12.7,13.0,13.2,13.5,13.8,14.1,14.3,14.6,14.6,14.2,13.4,12.6,11.7,11.0,11.2,12.0,13.1,14.1,15.2,15.9,15.2,13.7,12.0,11.4,10.9,10.5,10.2,10.1,9.8,9.4,8.9,8.3,7.9,7.7,7.4,7.2,7.0,7.1,7.6,8.3,9.5,10.9,12.5,13.8,13.4,12.3,10.6,9.4,8.1,6.7,6.2,6.0,5.6,4.9,4.0]
    # te = 0   
    # day = 29
    # for j in range(0,5):
    #     for i in range(0, 24):
    #         y = datetime(2022,12,day,i,0,0)
    #         yy = randint(0,100)
    #         pomiar = [y, tem[te],75]
    #         p = Temp(sensor_id = 125,time = y, temp = tem[te] , humi = yy )
    #         te += 1
    #         p.save()
    #         print(pomiar)
    #     day += 1
    #     print(day)
    return render(request, 'base/home.html')


@login_required(login_url='login')
def light(request):
    if request.method == 'POST':     
        get_data = json.loads(request.body)
        
        if get_data['action'] == 'change':
            return JsonResponse(change_light(get_data['id']))
        
    user_id = request.user.id    
    sensors = Sensor.objects.filter(fun = "light").filter(user_id = user_id)
    
    lights = []
    for sensor in sensors:
        lights.extend(Light.objects.filter(sensor_id = sensor.id))
            
    context = {
            'sensors': sensors,
            'lights': lights
    }
    return render(request,'base/light.html', context)


@login_required(login_url='login')
def chart(request):
    if request.method == 'POST':
        
        data_od = request.POST["dataod"]
        data_do = request.POST["datado"]
        place = request.POST["lista"]
        
        if len(data_od) == 0 or len(data_do) == 0:
            data_od = str(datetime.now() - timedelta(days=7))  # wyświetlenie danych z ostatnich 7 dni
            data_do = str(datetime.now())
            
        user_id = request.user.id
        list_place = Sensor.objects.filter(fun = 'temp').filter(user_id = user_id)
        
        context = data_for_chart(data_od, data_do, place)
        context['list_place'] = list_place
        return render(request,'base/chart.html',context)

    data_od = str(datetime.now() - timedelta(days=7))  # wyświetlenie danych z ostatnich 7 dni
    data_do = str(datetime.now())
    
    user_id = request.user.id
    list_place = Sensor.objects.filter(fun = 'temp').filter(user_id = user_id)
    
    if len(list_place) == 0:
         return render(request,'base/chart.html')
        
    place = list_place[0]
    context = data_for_chart(data_od, data_do, place)
    context['list_place'] = list_place
    return render(request,'base/chart.html', context)


@login_required(login_url='login')
def sensor(request):
    user_id = request.user.id
    
    if request.method == 'POST':
        get_data = json.loads(request.body)
        
        if get_data['action'] == 'add' and get_data['fun'] == 'uid' :
            return JsonResponse(add_uid(get_data))
        else:
            # sensor = Sensor(name=get_data['name'], ip="123.123.123.123", port="123", fun=get_data['fun'], user_id=user_id)
            # sensor.save()
            # sensor_id=Sensor.objects.filter(ip="123.123.123.123").get(user_id=user_id).id
            # respond = {'response': 'Udało sie dodać czujnik', 'id': sensor_id}  
            # print(respond)
            # return JsonResponse(respond)
            return JsonResponse(add_sensor(get_data,user_id))
    elif request.method == 'DELETE':
        get_data = json.loads(request.body)
        return JsonResponse(delete_sensor(get_data))
    
    sensors = Sensor.objects.filter(user_id=user_id)
    
    cards = []
    for sensor in sensors:
        if sensor.fun == 'rfid':
            cards.extend(Card.objects.filter(sensor_id = sensor.id))
                  
    context = {
                'sensors': sensors,
                'cards':cards}

    return render(request, 'base/sensor.html',context)


@login_required(login_url='login')
def stairs(request):
    if request.method == 'POST':
        get_data = json.loads(request.body)
        stairs = Stairs.objects.get(sensor_id=get_data['id'])
        sensor = Sensor.objects.get(id = get_data['id'])
        print(get_data)
        match get_data['action']:
            case 'set-lightingTime':
                stairs.lightTime = int(get_data['lightingTime'])
                message ='te'+str(get_data['lightingTime'])
            case 'set-brightness':
                stairs.brightness = int(get_data['brightness'])
                message = 'bs'+str(get_data['brightness'])
            case 'set-step':
                stairs.steps = int(get_data['step'])
                message = 'sp'+str(get_data['step'])
            case 'change-stairs':
                if stairs.mode:
                    stairs.mode = False
                    message = 'OFF'
                else:    
                    stairs.mode = True
                    message = 'ON'
        
        if send_data(message,sensor.ip,sensor.port):
            stairs.save()       
            stairs = Stairs.objects.filter(sensor_id=get_data['id']).values()
            return JsonResponse(stairs[0])
        else:
            return JsonResponse({'error':-1})
        
    user_id = request.user.id
    sensors = Sensor.objects.filter(fun="stairs").filter(user_id=user_id)
    context= {
        "sensors": sensors,
    }
    return render(request,'base/stairs.html',context)


@login_required(login_url='login')
def aquarium(request):
    if request.method == "POST":
        get_data = json.loads(request.body)
        
        
        aqua_id = get_data['id']
        sensor = Sensor.objects.get(id=aqua_id)
        aqua = Aqua.objects.get(sensor_id=aqua_id)
        
        message = ""
        response = {}
        
        match get_data['action']:
            case 'changeRGB':
                message = 'r'+str(get_data['r'])+'g' + str(get_data['g'])+ 'b' + str(get_data['b']) 
                aqua.color = message        
                    
            case 'changeLedTime':
                aqua.led_start = get_data['ledStart']
                aqua.led_stop = get_data['ledStop']    
                        
            case 'changeFluoLampTime':
                aqua.fluo_start = get_data['fluoLampStart']
                aqua.fluo_stop = get_data['fluoLampStop']

            case 'changeMode':
                aqua.mode = get_data['mode']
                if get_data['mode']:
                    response ={
                        'fluo': aqua.fluo_mode,
                        'led': aqua.led_mode
                    }
                    aqua.save()
                    return JsonResponse(response)
                else:
                    aqua.save()
                    
                
            case 'changeFluoLampState':
                if get_data['value']:
                    message = 's1'
                else:
                    message = 's0'
                aqua.fluo_mode=get_data['value']
                
            case 'changeLedState': 
                if get_data['value']:
                    message = 'r1'
                else:
                    message = 'r0'
                aqua.led_mode=get_data['value']
            
        # if message:
        #     if send_data(message, sensor.ip, sensor.port): 
        #         response = {'success': 1}
        #         aqua.save()   
        #     else:
        #         response= {'error': -1}
        # else:
        #     if checkAqua(sensor,aqua):
        #         response = {'success': 2}
        #         aqua.save()   
        #     else:
        #         response = {'error': -2}
                
        return JsonResponse(response)

    user_id = request.user.id
    aquas = Sensor.objects.filter(fun = 'aqua').filter(user_id=user_id)
    context = {
            'aquas':aquas
    }
    return render(request,'base/aquarium.html',context)


@login_required(login_url='login')
def sunblind(request):
    if request.method == 'POST':
        get_data = json.loads(request.body)
        print(get_data)
        ip_port = Sensor.objects.get(pk=get_data['id'])
        message = 'set'+str(get_data['value'])
        
        if send_data(message,ip_port.ip,ip_port.port):
            sunblind = Sunblind.objects.get(sensor_id = get_data['id'])
            sunblind.value = get_data['value']
            sunblind.save()  
            return JsonResponse({'success': 1})
        
        else:
            return JsonResponse({'error': -1})
        
        
    
    sunblinds = []
    user_id = request.user.id
    sensors = Sensor.objects.filter(fun = 'sunblind').filter(user_id=user_id)
    
    for sensor in sensors:
        sunblinds.extend(Sunblind.objects.filter(sensor_id = sensor.id))
        
    context = {
                'sensors': sensors,
                'sunblinds': sunblinds}
    return render(request,'base/sunblind.html', context)


@login_required(login_url='login')
def calibration(request, pk):
    if request.method == 'POST':
        get_data = json.loads(request.body)
        print(get_data)
        # ip_port = Sensor.objects.get(id=pk)
        # send_data(get_data['action'],ip_port.ip,ip_port.port)
        
        # if get_data['action'] == 'end':
        #     s = Sunblind.objects.get(sensor_id = pk)
        #     s.value = 100
        #     s.save()
            
    if request.method == 'GET':
        ip_port = Sensor.objects.get(id=pk)
        # send_data('calibration',ip_port.ip,ip_port.port)

    return render(request,'base/calibration.html')


@login_required(login_url='login')
def rpl(request):
    if request.method == 'POST':
        get_data = json.loads(request.body)
        print(get_data)
        if get_data['action'] == 'get':
            lamp = Sensor.objects.get(id = get_data['id'])
            rfids = Rfid.objects.filter(lamp = lamp.ip)
            buttons = Button.objects.filter(lamp = lamp.ip)
            
            rfid = [r.sensor_id for r in rfids ]
            btn = [b.sensor_id for b in buttons]
   
            respond = {'rfid': rfid,
                       'btn': btn}
            
            return JsonResponse(respond)
        
        elif get_data['action'] == 'connect':
            lamp = Sensor.objects.get(id = get_data['lamp'])   
            rfids = Rfid.objects.filter(lamp = lamp.ip)
            btns = Button.objects.filter(lamp = lamp.ip)
            
            btn_list = [b.sensor_id for b in btns]
            rfid_list =[r.sensor_id for r in rfids]   

            for id in get_data['rfids']:
                if int(id) not in rfid_list:
                    rfid = Rfid.objects.get(sensor_id = id)
                    rfid.lamp = lamp.ip
                    rfid.save()
                else:
                     rfid_list.remove(int(id))
                
            for id in rfid_list:
                rfid = Rfid.objects.get(sensor_id = id)
                rfid.lamp = ''
                rfid.save()
                
                
            for id in get_data['btns']:
                if int(id) not in btn_list:
                    btn = Button.objects.get(sensor_id=id)
                    btn.lamp = lamp.ip
                    btn.save()
                else:
                    btn_list.remove(int(id))
                
            for id in btn_list:
                btn = Button.objects.get(sensor_id=id)
                btn.lamp = ''
                btn.save()
                                
    user_id = request.user.id
    sensors = Sensor.objects.filter(user_id = user_id)
    context= {'sensors':sensors}
    return render(request,'base/rpl.html',context)