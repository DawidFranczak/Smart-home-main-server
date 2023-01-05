from datetime import datetime
from django.db.models import Q
import socket
from .models import *


# miesiac = 1
# dzien = 1
# godzina = 0
# pokoje=["Pokój","Garaż"]
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
#         pomiar = [(iddd, y, x, y,31)]
#         p = Temp(sensor_id = 31,time = y, temp = x , humi = yy )
#         p.save()
#         print(pomiar)
#         # data = "temp/" + i + str(x) + "/" + str(y)
#         # data = bytes(str(data), 'utf-8')
#         # print(data)
#         # sleep(0.01)
#         # sock.sendto(data, (str(socket.gethostbyname(socket.gethostname())), 1234))
#         godzina += 1
#         if (godzina == 24):
#             godzina = 0
#             dzien += 1
#         sleep(0.01)
#     dzien = 1
#     miesiac += 1

# ////////////////////////ADD///////////////////////////////////////////////////////////////

def add_sensor(get_data,user_id):
    '''
    Comunicate and save sensor
    '''
    
    match get_data['fun']:
        case 'temp':
            port = 1265
            message = str.encode('password_temp')
            answer = 'respond_temp'
        case 'sunblind':
            port = 9846
            message = str.encode('password_sunblind')
            answer = 'respond_sunblind'
        case 'light':
            port = 4324
            message = str.encode('password_light')
            answer = 'respond_light'
        case 'aqua':
            port = 7863
            message = str.encode('password_aqua')
            answer = 'respond_aqua'
        case 'stairs':
            port = 2965
            message = str.encode('password_stairs')
            answer = 'respond_stairs'
        case 'rfid':
            port = 3984
            message = str.encode('password_rfid')
            answer = 'respond_rfid'
        case 'btn':
            port = 7894
            message = str.encode('password_btn')
            answer = 'respond_btn'
        case 'lamp':
            port = 4569
            message = str.encode('password_lamp')
            answer = 'respond_lamp'
        
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for i in range(2,254):
        checkip = '192.168.0.'+str(i)
        
        try:
            sock.sendto(message, (checkip, port))
            sock.settimeout(0.05)
            data = sock.recvfrom(128)
            response = data[0].decode('UTF-8')
            
            if response == answer:
                response_sensor_ip = str(data[1][0])
                
                if Sensor.objects.filter(ip = response_sensor_ip).exists():
                    respond = {'response': 'Czujnik już dodano'}
                    return respond

                sensor = Sensor(name=get_data['name'], ip=response_sensor_ip, port=port, fun=get_data['fun'], user_id=user_id)
                sensor.save()
                sensor_id = Sensor.objects.filter(ip=response_sensor_ip).get(user_id=user_id).id
                
                match get_data['fun']:
                    case 'aqua':
                        aqua = Aqua(sensor_id = sensor_id)
                        aqua.save()
                    case 'light':
                        light = Light(sensor_id = sensor_id, light = False)
                        light.save()
                    case 'sunblind':
                        sensor = Sunblind(sensor_id = sensor_id, value = 0)
                        sensor.save()
                    case 'stairs':
                        sensor = Stairs(sensor_id = sensor_id)
                        sensor.save()
                    case 'btn':
                        btn = Button(sensor_id = sensor_id)
                        btn.save()
                    case 'rfid':
                        rfid = Rfid(sensor_id = sensor_id)
                        rfid.save()
                respond = {'response': 'Udało sie dodać czujnik', 'id': sensor_id}  
                sock.close()
                return respond
                
        except Exception as e:
            print(e)
            continue
        
    else:
        respond = {'response': 'Nie udało się zapisać czujnika'}
        sock.close()
        return respond


def add_uid(_data):
    '''
        Add new rfid card to user
    '''
    
    respond = {}
    try:
        sensor = Sensor.objects.get(id = _data['id'])
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # INTERNET / UDP
            sock.bind(('', 6721))
        except Exception as e:
            respond = {'response': 'Nie udało się otworzyć socketu'}
            return respond
            
        wiad = str.encode('add-tag')
        sock.sendto(wiad, (sensor.ip, sensor.port))
        sock.settimeout(9)
        data = sock.recvfrom(128)
        uid = int(data[0].decode('UTF-8'))
        sock.close()
                
        if Card.objects.filter(uid=uid).exists():
            respond = {'response': 'Ta karta jest już dodana'} 
            return respond
        
        card = Card(sensor_id = sensor.id, uid = uid, name = _data['name'] )
        card.save()
        respond = {'response': 'Udało sie dodać czujnik', 'id': card.id} 
            
    except Exception as e:
        print(e)
        respond = {'response': 'Nie udało dodać się czujnika'} 
        sock.close()
    return respond


# # ///////////////////////DELETE/////////////////////////////////////////
def delete_sensor(get_data):
    '''
    Delete user sensor
    '''
    try:
        sensor = str(get_data['id'])
        if sensor.startswith('card'):
            Card.objects.filter(id=get_data['id'].split(' ')[1]).delete()
            response = {'response': 'permission'}
            return response
        else:
            Sensor.objects.get(id=get_data['id']).delete()
            response = {'response': 'permission'}
    except:
        response = {'response': 'Nie udało się usunąć czujnika'}
    return response


# # /////////////////////////REST/////////////////////////////////////////
def data_for_chart(data_from, data_to, place):
    ''' 
    Get data and avarage temperature for chart from date to date
    '''
    
    data_temp = []
    data_time = []
    data_average_temp_day = []
    data_average_temp_night = []
    data_average_data = []
    average_day = []
    average_night = []
    
    start_day = '06'
    end_day = '18'

    temps = Temp.objects.filter(
        Q(sensor_id = Sensor.objects.get(name=place)) &
        Q(time__gte = data_from) &
        Q(time__lte = data_to))

    date_old = str(temps[0])[:10]
    for temp in temps:
        date_new = str(temp)[:10]
        if str(temp.time) <= data_to and str(temp.time) >= str(data_from):
            data_temp.append(temp.temp)
            data_time.append(str(temp.time)[:16])
            hour = str(temp.time).split().pop(1)[:2]
            
            if hour > start_day and hour <= end_day:
                average_day.append(float(temp.temp))
            else:
                average_night.append(float(temp.temp))
                   
        if date_new != date_old:
            
            data_average_temp_day.append(
                round(sum(average_day) /len(average_day), 2)) 
            data_average_temp_night.append(
                round(sum(average_night) / len(average_night), 2)) 

            data_average_data.append(date_old)
            
            average_day.clear()
            average_night.clear()
            date_old = date_new
            
    context = {
            'data_temp': data_temp,
            'data_time': data_time,
            'data_average_temp_day': data_average_temp_day,
            'data_average_temp_night': data_average_temp_night,
            'data_average_data': data_average_data,
            'place': place,
            }                
    return context


def change_light(id):
    '''
    communicate with lamp and try to change it state
    '''
    try:
        sensor = Sensor.objects.get(id=id)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # INTERNET / UDP
        wiad = str.encode('change')
        sock.sendto(wiad, (sensor.ip, 4324))
        sock.settimeout(1)
        data = sock.recvfrom(128)
        data = data[0].decode('UTF-8')        
        light = Light.objects.get(sensor_id = sensor.id)
        
        if data == 'ON':
            light.light = True
            response = {'response': 1}
        else:
            light.light = False
            response = {'response': 0}
        light.save() 
    except TimeoutError:
        response = {'response': -1}
    finally: 
        sock.close()
        return response
        
     
def send_data(_mess, _ip, _port):
    '''
    Send message to microcontroler on _port and _ip 
    '''
    try:
        wiad = str.encode(_mess)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # INTERNET / UDP
        sock.sendto(wiad, (_ip, _port))
        sock.close()
        return True
    except:
        sock.close()
        return False

    
def checkAqua(sensor,aqua):
    '''
    Turn on or turn off fluo lamp and led dependence on time
    and save it to database
    '''
    
    if datetime.now().hour < 10:
        hours = '0' + str(datetime.now().hour)
    else:
        hours = str(datetime.now().hour)
   
    if datetime.now().minute < 10:
        minutes = ':0' + str(datetime.now().minute) + ':' + str(datetime.now().second)
    else:
        minutes = ':' + str(datetime.now().minute) + ':' + str(datetime.now().second)
        
    time_now = hours + minutes
    led_start = str(aqua.led_start)
    led_stop = str(aqua.led_stop)
    fluo_start = str(aqua.fluo_start)
    fluo_stop = str(aqua.fluo_stop)
    
    if led_start < time_now and led_stop > time_now:
        led = 'r1'
        aqua.led_mode=True  
    else:
        led = 'r0'
        aqua.led_mode=False
    aqua.save() 
    
    if send_data(led,sensor.ip,sensor.port):
        
        if fluo_start < time_now and fluo_stop > time_now:
            fluo = 's1'
            aqua.fluo_mode=True
        else:
            fluo = 's0'
            aqua.fluo_mode=False
        aqua.save()
        
        if send_data(fluo, sensor.ip, sensor.port):
            return True
    
