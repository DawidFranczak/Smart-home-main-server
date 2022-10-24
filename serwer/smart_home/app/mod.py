from datetime import datetime, timedelta
import socket
from .models import *


# ////////////////////////////
#   miesiac = 1
#     dzien = 1
#     godzina = 0
#     pokoje=["Pokój","Garaż"]
#     iddd = 1
#     for i in range(12):
#         while(dzien != 32):
#             try:
#                 y = datetime(2022,miesiac,dzien,godzina,0,0)
#                 # print(y)
#             except ValueError:
#                 dzien = 1
#                 miesiac += 1
#                 godzina = 0
#             x = randint(0,20)
#             yy = randint(0,100)
#             iddd += 1
#             pomiar = [(iddd, y, x, y,31)]
#             p = Temp(sensor_id = 31,time = y, temp = x , humi = yy )
#             p.save()
#             print(pomiar)
#             # data = "temp/" + i + str(x) + "/" + str(y)
#             # data = bytes(str(data), 'utf-8')
#             # print(data)
#             # sleep(0.01)
#             # sock.sendto(data, (str(socket.gethostbyname(socket.gethostname())), 1234))
#             godzina += 1
#             if (godzina == 24):
#                 godzina = 0
#                 dzien += 1
#             sleep(0.01)
#         dzien = 1
#         miesiac += 1



# ////////////////////////// GET/////////////////////////////////////////////////////////
# def get_settings(place):
#     con = sqlite3.connect('db/pomiar2.db')  # otwarcie bazy danych
#     cur = con.cursor()
#     settings = []
#     for i in cur.execute('SELECT value FROM ls WHERE name = ?', (place,)):
#         settings = i[0]
#     cur.close()
#     return settings


# def get_chart_place():
#     sensors = Sensor.objects.filter(fun='temp')
#     return sensors


# def get_sensor_ip(_id):
    
#     con = sqlite3.connect('db/pomiar2.db')  # otwarcie bazy danych
#     cur = con.cursor()
#     for i in cur.execute('SELECT ip, port FROM sensor WHERE id = ?', (_id,)):
#         ip = i[0]
#         port = i[1]
#     cur.close()
#     return ip, port



# /////////////////////////SAVE/////////////////////////////////////////////////////////
# def save_settings(_value, _id):
#     try:
#         wiad = str.encode(_value)
#         sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # INTERNET / UDP
#         ip, port = get_sensor_ip(_id)
#         sock.sendto(wiad, (str(ip), port))
#         sock.close()
        
#         con = sqlite3.connect('db/pomiar2.db')  # otwarcie bazy danych
#         cur = con.cursor()
#         cur.execute(""" UPDATE sensor SET value = ? WHERE id = ? """, (_value, _id))
#         con.commit()
#         con.close()
#         print(f"zapisano w {_id} wartosc {_value}")
#     except socket.gaierror:
#         sock.close()
#         print("nie udało się wysłąć")
#     except:
#         return "coś poszło nie tak"


# ////////////////////////ADD///////////////////////////////////////////////////////////////

def add_sensor(get_data):
    if get_data["fun"] == "temp":
        port = 1265
        wiad = str.encode("password_temp")
        ans = "respond_temp"
        
    elif get_data["fun"] =="sunblind":
        port = 9846
        wiad = str.encode("password_sunblind")
        ans = "respond_sunblind"
        
    elif get_data["fun"] =="light":
        port = 4324
        wiad = str.encode("password_light")
        ans = "respond_light"
        
    elif get_data["fun"] == "aqua":
        port = 7863
        wiad = str.encode("password_aqua")
        ans = "respond_aqua"
        
    elif get_data["fun"] == "stairs":
        port = 2965
        wiad = str.encode("password_stairs")
        ans = "respond_stairs"
        
    elif get_data["fun"] == "rfid":
        port = 3984
        wiad = str.encode("password_rfid")
        ans = "respond_rfid"
        
    elif get_data["fun"] =="btn":
        port = 7894
        wiad = str.encode("password_btn")
        ans = "respond_btn"
        
    elif get_data["fun"] =="lamp":
        port = 4569
        wiad = str.encode("password_lamp")
        ans = "respond_lamp"
        
    ipList = []        
    sensors = Sensor.objects.all()
    for sensor in sensors:
        ipList.append(sensor.ip)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # INTERNET / UDP
    for i in range(2,254):
        checkip = "192.168.0."+str(i)
        try:
            sock.sendto(wiad, (checkip, port))
            sock.settimeout(0.05)
            data = sock.recvfrom(128)
            if data[0].decode("UTF-8") == ans:
                if data[1][0] not in ipList:
                    s = Sensor(name=get_data['name'], ip=str(data[1][0]), port=port, fun=get_data['fun'] )
                    s.save()
                    sensor_id=Sensor.objects.get(ip=str(data[1][0])).id
                    if get_data['fun'] == 'aqua':
                        a = Aqua(sensor_id = sensor_id)
                        a.save()
                    elif get_data['fun'] == 'light':
                        l = Light(sensor_id = sensor_id, light = False)
                        l.save()
                    elif get_data['fun'] == 'sunblind':
                        s = Sunblind(sensor_id = sensor_id, value = 0)
                        s.save()
                    elif get_data['fun'] == 'stairs':
                        s = Stairs(sensor_id = sensor_id)
                        s.save()
                    elif get_data['fun'] == 'btn':
                        b = Button(sensor_id = sensor_id)
                        b.save()
                    elif get_data['fun'] == 'rfid':
                        r = Rfid(sensor_id = sensor_id)
                        r.save()
    
                    respond = {"response": "Udało sie dodać czujnik", "id": sensor_id}  
                    sock.close()
                    return respond
        except Exception as e:
            print(e)
            pass
    else:
        respond = {"response": "Nie udało się zapisać czujnika"}
        sock.close()
        return respond

def add_uid(_data):
    respond = {}
    try:
        r = Sensor.objects.get(id = _data['id'])
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # INTERNET / UDP
            sock.bind(('', 6721))
        except Exception as e:
            print(e)
            # pass
        wiad = str.encode("add-tag")
        sock.sendto(wiad, (r.ip, r.port))
        sock.settimeout(9)
        data = sock.recvfrom(128)
        data = int(data[0].decode('UTF-8'))
        print(data)
        sock.close()
        cards = Card.objects.filter(sensor_id = _data['id'])
        for card in cards:
            print(card.uid)
            if data == card.uid:
                respond = {"response": "Kartę już dodano do tego czujnika"} 
                return respond
        else:
            u = Card(sensor_id = r.id, uid = data, name = _data['name'] )
            u.save()
            respond = {"response": "Udało sie dodać czujnik", "id": u.id} 
    except Exception as e:
        print(e)
        pass
    except:
        respond = {"response": "Nie udało dodać się czujnika"} 
    return respond

# # ///////////////////////DELETE/////////////////////////////////////////
def delete_sensor(get_data):
    if get_data['id'].split(" ")[0]== 'card':
        Card.objects.filter(id=get_data['id'].split(" ")[1]).delete()
        response = {"response": "permission"}
        return response
    try:
        Sensor.objects.get(id=get_data['id']).delete()
        response = {"response": "permission"}
    except:
        response = {"response": "Nie udało się usunąć czujnika"}
    return response

# # /////////////////////////REST/////////////////////////////////////////
def data_for_chart(data_od, data_do, place):
    data_temp = []
    data_time = []
    data_average_temp_day = []
    data_average_temp_night = []
    data_average_data = []
    average_day = 0
    average_night = 0
    d = 0
    d2 = 0
    start_day = "06"
    end_day = "18"
    format = '%Y-%m-%d'

    try:
        data_do = datetime.strptime(data_do, format) + timedelta(days=1)
    except ValueError:
        pass
    temps = Temp.objects.filter(sensor_id=Sensor.objects.get(name=place))
    for temp in temps:  # wyciągnięcie danych z bazy dancyh
        if str(temp.time) <= str(data_do) and str(temp.time) >= str(data_od):
            data_temp.append(temp.temp)
            data_time.append(str(temp.time)[:16])
            if str(temp.time).split().pop(1)[:2] > start_day and str(temp.time).split().pop(1)[:2] <= end_day:
                average_day = average_day + float(temp.temp)
                d += 1
                if d == 12:
                    data_average_temp_day.append(
                        round(average_day / d, 2))  # zaokrąglanie liczby do 2 miejscpo przecinku oraz wpisanie do listy
                    data_average_data.append(str(temp.time)[:10])
                    average_day = 0
                    d = 0
            else:
                average_night = average_night + float(temp.temp)
                d2 += 1
                if d2 == 12:
                    data_average_temp_night.append(
                        round(average_night / d2, 2))  # zaokrąglanie liczby do 2 miejscpo przecinku oraz wpisanie do listy
                    average_night = 0
                    d2 = 0 
    return data_temp, data_time, data_average_temp_day, data_average_temp_night, data_average_data


def change_light(id):
    try:
        s = Sensor.objects.get(id=id)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # INTERNET / UDP
        wiad = str.encode("change")
        sock.sendto(wiad, (s.ip, 4324))
        sock.settimeout(1)
        data = sock.recvfrom(128)
        data = data[0].decode('UTF-8')
        sock.close()
        if data == "ON":
            l = Light.objects.get(sensor_id = s.id)
            l.light = True
            l.save()
            return {'response': 1}
            
        else:
            l = Light.objects.get(sensor_id = s.id)
            l.light = False
            l.save()
            return {'response': 0}
            
    except InterruptedError as e:
        # print(e)
        pass
     
    
def send_data(_mess, _ip, _port):
    try:
        wiad = str.encode(_mess)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # INTERNET / UDP
        sock.sendto(wiad, (_ip, _port))
        sock.close()
    except:
        sock.close()
        return "Nie udało się wysłać"
    
def checkAqua(sensor,aqua):
    if datetime.now().hour < 10:
        hours = "0"+str(datetime.now().hour)
    else:
        hours = str(datetime.now().hour)
   
    if datetime.now().minute < 10:
        minutes = ":0"+str(datetime.now().minute)+ ':'+ str(datetime.now().second)
    else:
        minutes = ":"+str(datetime.now().minute)+ ':'+ str(datetime.now().second)
        
    timeNow = hours + minutes
    ledStart = str(aqua.led_start)
    ledStop = str(aqua.led_stop)
    fluoStart = str(aqua.fluo_start)
    fluoStop = str(aqua.fluo_stop)
    print(aqua.led_mode)
    

    if ledStart < timeNow and ledStop > timeNow:
        led = 'r1'
        print(led)
        aqua.led_mode=True  
    else:
        led = 'r0'
        print(led)
        aqua.led_mode=False
    aqua.save()
        
      
    if fluoStart < timeNow and fluoStop > timeNow:
        fluo = 's1'
        print(fluo)
        aqua.fluo_mode=True
    else:
        fluo = 's0'
        print(fluo)
        aqua.fluo_mode=False
    aqua.save()
           
    send_data(led,sensor.ip,sensor.port)
    send_data(fluo,sensor.ip,sensor.port)