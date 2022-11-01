from email.errors import MessageParseError
from inspect import Attribute
from multiprocessing import context
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


from speaker import checkAquaAll
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
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Użytkownik nie istenieje.')
            return redirect('login')
        
        user = authenticate(request, username=username, password=password)
        
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
    #     login = request.form["login"]
    #     haslo = request.form["haslo"]
    # context = {}
    # s = Temp(sensor_id=Sensor.objects.get(name = 'room').id ,temp = '11', humi = '122')
    # s.save()
    # sensor = Sensor.objects.all()
    # sensor = Sensor.objects.get(name = 'room').id

    # context = {'sensor': sensor}
    
    return render(request, 'main.html')


@login_required(login_url='login')
def light(request):
    if request.method == 'POST':     
        get_data = json.loads(request.body)
        if get_data['action'] == 'change':
            return JsonResponse(change_light(get_data['id']))
        
    sensors = Sensor.objects.filter(fun = "light")
    lights = Light.objects.all()
    context = {
            'sensors': sensors,
            "lights":lights
    }
    
    print(request.user.id)
    return render(request,'base/light.html', context)


@login_required(login_url='login')
def wykres(request):
    if request.method == 'POST':
        data_od = request.POST["dataod"]
        data_do = request.POST["datado"]
        place = request.POST["lista"]
        if len(data_od) == 0 or len(data_do) == 0:
            data_od = str(datetime.now() - timedelta(days=7))  # wyświetlenie danych z ostatnich 7 dni
            data_do = str(datetime.now())
        list_place = Sensor.objects.filter(fun = 'temp')
        
        data_temp, data_time, data_average_temp_day, data_average_temp_night, \
            data_average_data= data_for_chart(data_od, data_do, place)
        context = {
            "data_temp":data_temp,
            "data_time":data_time,
            "data_average_temp_day":data_average_temp_day,
            "data_average_temp_night":data_average_temp_night,
            "data_average_data":data_average_data,
            "place":place,
            "list_place":list_place,
            }
        return render(request,'base/wykres.html',context)

    data_od = str(datetime.now() - timedelta(days=7))  # wyświetlenie danych z ostatnich 7 dni
    data_do = str(datetime.now())
    list_place = Sensor.objects.filter(fun = 'temp')
    if len(list_place) == 0:
         return render(request,'base/wykres.html')
        
    place = list_place[0]
    data_temp, data_time, data_average_temp_day, data_average_temp_night, \
        data_average_data = data_for_chart(data_od, data_do, place)
    context = {
                "data_temp":data_temp,
                "data_time":data_time,
                "data_average_temp_day":data_average_temp_day,
                "data_average_temp_night":data_average_temp_night,
                "data_average_data":data_average_data,
                "place":place,
                "list_place":list_place,
                'title':'Temperatura'
    }
    return render(request,'base/wykres.html', context)


@login_required(login_url='login')
def sensor(request):
    if request.method == "POST":
        get_data = json.loads(request.body)
        
        if get_data["action"] == "add" and get_data["fun"] == "uid" :
            return JsonResponse(add_uid(get_data))
        else:
            return JsonResponse(add_sensor(get_data))
        
    elif request.method == "DELETE":
        get_data = json.loads(request.body)
        return JsonResponse(delete_sensor(get_data))
    
    sensors = Sensor.objects.all()
    cards = Card.objects.all()
    context = {
                'sensors': sensors,
                'cards':cards}

    return render(request, 'base/sensor.html',context)


@login_required(login_url='login')
def stairs(request):
    if request.method == "POST":
        get_data = json.loads(request.body)
        print(get_data)
        stairs = Stairs.objects.get(sensor_id=get_data['id'])
        sensor = Sensor.objects.get(id = get_data['id'])
        match get_data['action']:
            
            case 'set-lightingTime':
                stairs.lightTime = int(get_data['lightingTime'])
                stairs.save()
                send_data("te"+str(get_data['lightingTime']),sensor.ip,sensor.port)
                
            case 'set-brightness':
                stairs.brightness = int(get_data['brightness'])
                stairs.save()
                send_data("bs"+str(get_data['brightness']),sensor.ip,sensor.port)
                
            case 'set-step':
                stairs.steps = int(get_data['step'])
                stairs.save()
                send_data("sp"+str(get_data['step']),sensor.ip,sensor.port)
            
            case 'change-stairs':
                if stairs.mode:
                    stairs.mode = False
                    stairs.save()
                    send_data("OFF",sensor.ip,sensor.port)
                else:    
                    stairs.mode = True
                    stairs.save()
                    send_data("ON",sensor.ip,sensor.port)
                
        # stairs = json.dumps(stairs)
        stairs = Stairs.objects.filter(sensor_id=get_data['id']).values()
        return JsonResponse(stairs[0])

    
    
    sensors = Sensor.objects.filter(fun="stairs")
    stairses = Stairs.objects.all()
    context= {
        "sensors": sensors,
        "stairses": stairses
    }
    return render(request,'base/stairs.html',context)


@login_required(login_url='login')
def akwarium(request):
    if request.method == "POST":
        get_data = json.loads(request.body)
        sensor = Sensor.objects.get(id=get_data['id'])
        aqua = Aqua.objects.get(sensor_id = get_data['id'])
        match get_data['action']:
            
            case 'changeRGB':
                message = "r"+str(get_data['r'])+"g" + str(get_data['g'])+ "b" + str(get_data['b'])
                send_data(message, sensor.ip, sensor.port)
                aqua.color = message
            
            case 'changeLedTime':
                aqua.led_start = get_data['ledStart']
                aqua.led_stop = get_data['ledStop']
                checkAqua(sensor,aqua)
                
            case 'changeFluoLampTime':
                aqua.fluo_start = get_data['fluoLampStart']
                aqua.fluo_stop = get_data['fluoLampStop']
                checkAqua(sensor,aqua)
                
            case 'changeMode':
                aqua.mode = get_data['mode']
                if get_data['mode'] == False:
                    checkAqua(sensor,aqua)
                else:
                    aqua.save()
                    dict = {
                        'fluo': aqua.fluo_mode,
                        'led' : aqua.led_mode
                    }
                    return JsonResponse(dict)
                    
            case 'changeFluoLampState':
                if get_data['value'] == True:
                    mess = "s1"
                else:
                    mess = "s0"
                send_data(mess, sensor.ip, sensor.port)
                aqua.fluo_mode=get_data['value']
                
            case 'changeLedState': 
                if get_data['value'] == True:
                    mess = "r1"
                else:
                    mess = "r0"
                send_data(mess, sensor.ip, sensor.port)
                aqua.led_mode=get_data['value']
            
        aqua.save()   
        return render(request,'base/akwarium.html') 

    aquas = Sensor.objects.filter(fun = "aqua")
    context = {
            "aquas":aquas
    }
    return render(request,'base/akwarium.html',context)


@login_required(login_url='login')
def rolety(request):
    if request.method == "POST":
        get_data = json.loads(request.body)
        ip_port = Sensor.objects.get(pk=get_data["id"])
        mess = "set"+str(get_data['value'])
        send_data(mess,ip_port.ip,ip_port.port)
        s = Sunblind.objects.get(sensor_id = get_data["id"])
        s.value = get_data['value']
        s.save()  
    sensors = Sensor.objects.filter(fun = 'sunblind')
    sunblinds = Sunblind.objects.all()
    context = {
                'sensors': sensors,
                'sunblinds': sunblinds}
    return render(request,'base/rolety.html', context)


@login_required(login_url='login')
def calibration(request, pk):
    if request.method == 'POST':
        get_data = json.loads(request.body)
        ip_port = Sensor.objects.get(id=pk)
        send_data(get_data["action"],ip_port.ip,ip_port.port)
        if get_data["action"] == "end":
            s = Sunblind.objects.get(sensor_id = pk)
            s.value = 100
            s.save()
            
    if request.method == 'GET':
        ip_port = Sensor.objects.get(id=pk)
        send_data("calibration",ip_port.ip,ip_port.port)

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
            
            rfid = []
            btn = []
            for b in buttons:
                print(b.sensor_id)
                btn.append(b.sensor_id)
            for r in rfids:
                rfid.append(r.sensor_id)
                
            respond = {'rfid':rfid,
                       'btn':btn}
            print(respond)
            return JsonResponse(respond)
        
        elif get_data['action'] == 'connect':
            lamp = Sensor.objects.get(id = get_data['lamp'])   
            rfids = Rfid.objects.filter(lamp = lamp.ip)
            btns = Button.objects.filter(lamp = lamp.ip)
            btn_list = []
            rfid_list =[]
            
            for rfid in rfids:
                rfid_list.append(rfid.sensor_id)     

            for id in get_data["rfids"]:
                if int(id) not in rfid_list:
                    r = Rfid.objects.get(sensor_id = id)
                    r.lamp = lamp.ip
                    r.save()
                else:
                     rfid_list.remove(int(id))
                
            for id in rfid_list:
                r = Rfid.objects.get(sensor_id = id)
                r.lamp = ''
                r.save()
                
            for btn in btns:
                btn_list.append(btn.sensor_id)    
                
            for id in get_data['btns']:
                if int(id) not in btn_list:
                    b = Button.objects.get(sensor_id=id)
                    b.lamp = lamp.ip
                    b.save()
                else:
                    btn_list.remove(int(id))
                
            for id in btn_list:
                b = Button.objects.get(sensor_id=id)
                b.lamp = ''
                b.save()
                
        
        
    sensors = Sensor.objects.all()
    context= {'sensors':sensors}
    return render(request,'base/rpl.html',context)