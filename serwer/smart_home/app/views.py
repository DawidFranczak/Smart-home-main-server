from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from datetime import datetime, timedelta
import json

from .forms import CreateUserForm, ChangePasswordForm, ChangeEmailForm, ChangeImageForm
from .models import *
from .mod import *


# Create your views here.

def user_register(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            form.save()  
            messages.success(request,'Rejestracja przebiegła pomyślnie.')
            return redirect('login') 
        
    context = {'form': form}
    return render(request, 'base/register.html', context)


def user_login(request):
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


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def user_page(request):
    return render(request, 'base/user_page.html')


@login_required(login_url='login')
def user_change_password(request):
    form = ChangePasswordForm(request.user)
    if request.method == 'POST':
        form = ChangePasswordForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            username = request.user
            password = request.POST.get('new_password1')
            user = authenticate(request, username=username, password=password)
            login(request,user)  
            messages.success(request,'Zmiana hasła przebiegła pomyślnie')
            return redirect('user_page')
    context = {'action':'password',
              'form':form}
    
    return render(request, 'base/user_page.html',context)


@login_required(login_url='login')
def user_change_email(request):
    form = ChangeEmailForm(request.user)
    old = request.user.email
    if request.method =='POST':
        form = ChangeEmailForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Zmiana emaila przebiegła pomyślnie')
            return redirect('user_page')
        
    context = {'action':'email',
              'form':form,
              'old':old}
    
    return render(request, 'base/user_page.html',context)
   
   
@login_required(login_url='login')
def user_change_image(request):
    form = ChangeImageForm(request.user)
    if request.method == 'POST':
        form = ChangeImageForm(request.user, request.POST, request.FILES)
        if request.POST.get('save') is not None:
            if form.is_valid():
                form.save()
                messages.success(request, 'Udało się zmienić zdjęcie(a)')
                return redirect('user_page')
        else:
            form.reset()
            messages.success(request, 'Zresetowano zdjęcia')
            return redirect('user_page')
        
    context = {'action':'image',
               'form': form}
    
    return render(request, 'base/user_page.html',context) 


@login_required(login_url='login')
def home(request):
    nav = HomeNavImage.objects.get(user_id = request.user.id)
    context = {'image': nav}
    return render(request, 'base/home.html', context)


@login_required(login_url='login')
def light(request):
    if request.method == 'POST':     
        get_data = json.loads(request.body)
        if get_data['action'] == 'change':
            return JsonResponse(change_light(get_data['id']))
        
    user_id = request.user.id    
    sensors = Sensor.objects.filter(fun = "light").filter(user_id = user_id)
    lights_2d = [Light.objects.filter(sensor_id = sensor.id) for sensor in sensors] 
    lights = [light for light_ in lights_2d for light in light_]
    
    context = {
            'sensors': sensors,
            'lights': lights
              }
    
    return render(request,'base/light.html', context)


@login_required(login_url='login')
def chart(request):
    user_id = request.user.id
    list_place = Sensor.objects.filter(fun = 'temp').filter(user_id = user_id)
    
    if len(list_place) == 0:
         return render(request,'base/chart.html')
    
    data_from = str(datetime.now().date() - timedelta(days=6))
    data_to = str(datetime.now())

    
    if request.method == 'POST':
        if request.POST["data-from"] and request.POST["data-to"]:
            data_from = request.POST["data-from"]
            data_to = request.POST["data-to"]
            format = '%Y-%m-%d'
            data_to = str(datetime.strptime(data_to[:19], format) + timedelta(days=1))
            
        place = request.POST["list"]
        context = data_for_chart(data_from, data_to, place)
        context['list_place'] = list_place
        return render(request,'base/chart.html',context)

    place = list_place[0]
    context = data_for_chart(data_from, data_to, place)
    context['list_place'] = list_place
    return render(request,'base/chart.html', context)


@login_required(login_url='login')
def sensor(request):
    user_id = request.user.id
    
    match request.method:
        case 'POST':
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
            
        case 'DELETE':
            get_data = json.loads(request.body)
            return JsonResponse(delete_sensor(get_data))

        case 'GET':
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
            
        if message:
            if send_data(message, sensor.ip, sensor.port): 
                response = {'success': 1}
                aqua.save()   
            else:
                response= {'error': -1}
        else:
            if checkAqua(sensor,aqua):
                response = {'success': 2}
                aqua.save()   
            else:
                response = {'error': -2}
                
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
        ip_port = Sensor.objects.get(pk=get_data['id'])
        message = 'set' + str(get_data['value'])
        
        if send_data(message,ip_port.ip,ip_port.port):
            sunblind = Sunblind.objects.get(sensor_id = get_data['id'])
            sunblind.value = get_data['value']
            sunblind.save()  
            return JsonResponse({'success': 1})
        
        else:
            return JsonResponse({'error': -1})
        
    user_id = request.user.id
    sensors = Sensor.objects.filter(fun = 'sunblind').filter(user_id=user_id)
    
    sunblinds = []

    for sensor in sensors:
        sunblinds.extend(Sunblind.objects.filter(sensor_id = sensor.id))
        
    context = {
                'sensors': sensors,
                'sunblinds': sunblinds
                }
    return render(request,'base/sunblind.html', context)


@login_required(login_url='login')
def calibration(request, pk):
    if request.method == 'POST':
        get_data = json.loads(request.body)
        ip_port = Sensor.objects.get(id=pk)
        send_data(get_data['action'], ip_port.ip, ip_port.port)
        
        if get_data['action'] == 'end':
            s = Sunblind.objects.get(sensor_id = pk)
            s.value = 100
            s.save()
            
    elif request.method == 'GET':
        ip_port = Sensor.objects.get(id=pk)
        send_data('calibration', ip_port.ip, ip_port.port)

    return render(request,'base/calibration.html')


@login_required(login_url='login')
def rpl(request):
    if request.method == 'POST':
        get_data = json.loads(request.body)
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
            
            btn_list = set([b.sensor_id for b in btns])
            rfid_list = set([r.sensor_id for r in rfids])
            btn_add = set([int(i) for i in get_data['btns']])
            rfid_add = set([int(i) for i in get_data['rfids']])
            
            for id in rfid_add:
                if id not in rfid_list:
                    rfid = Rfid.objects.get(sensor_id = id)
                    rfid.lamp = lamp.ip
                    rfid.save()
                else:
                     rfid_list.remove(id)
                
            for id in rfid_list:
                rfid = Rfid.objects.get(sensor_id = id)
                rfid.lamp = ''
                rfid.save()
                
                
            for id in btn_add:
                if id not in btn_list:
                    btn = Button.objects.get(sensor_id=id)
                    btn.lamp = lamp.ip
                    btn.save()
                else:
                    btn_list.remove(id)
                
            for id in btn_list:
                btn = Button.objects.get(sensor_id=id)
                btn.lamp = ''
                btn.save()
                                
    user_id = request.user.id
    sensors = Sensor.objects.filter(user_id = user_id)
    context= {'sensors':sensors}
    return render(request,'base/rpl.html',context)