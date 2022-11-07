import sqlite3
import socket
from datetime import datetime
from email.message import EmailMessage
import smtplib 


def add_temp_measurment(place, temp,humi):
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    pomiar = [(temp,humi,place,datetime.now())]
    cur.executemany("INSERT INTO app_temp(temp,humi,sensor_id,time) VALUES (?,?,?,?)", pomiar)
    con.commit()
    cur.close()
    print("{}".format(pomiar))


def measurement_temp():
    con = sqlite3.connect('db.sqlite3')  # otwarcie bazy danych
    cur = con.cursor()
    ip = []
    port = []
    place = []
    sensor_id =[]
    
    for i in cur.execute('SELECT ip, port,name,id FROM app_sensor WHERE fun = "temp"'):
        ip.append(i[0])
        port.append(i[1])
        place.append(i[2])
        sensor_id.append(i[3])
        
    cur.close()
    timeout = []
    not_connected = []
    wiad = str.encode("pomiar")
    temp = ""
    # print(ip, port, place)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # INTERNET / UDP
    for i in range(0, len(ip)):
        try:
            print(f"wysyłam do {place[i]}")
            sock.sendto(wiad, (ip[i], port[i]))
            sock.settimeout(1)
            data_rec = sock.recvfrom(1024)
            measurement = data_rec[0].decode("UTF-8")
            print(f"Dokonano pomiaru w miejscu : {place[i]}, pomiar : {temp}")
            temp = measurement.split('/')[0]
            humi = measurement.split('/')[1]
            add_temp_measurment(sensor_id[i], temp,humi)
            
        except socket.timeout:
            print(f"timeout {place[i]}")
            timeout.append(place[i])
            
        except Exception as e:
            print(e)
            not_connected.append(place[i])
            print(f"not connected {place[i]}")

    sock.close()

    if len(timeout) and len(not_connected):
        wiad = "Nie udało się odczytać wartości z czujników "
        
        for i in range(0, len(timeout)):
            if i == len(timeout) - 1:
                wiad += timeout[i] + ". "
            else:
                wiad += timeout[i] + ", "
                
        wiad += "Nie udało sie połączyć z "
        
        for i in range(0, len(not_connected)):
            if i == len(not_connected) - 1:
                wiad += not_connected[i] + ". "
            else:
                wiad += not_connected[i] + ", "
                print(wiad)
        send_email("Błąd odczytu temperatury", wiad)
        
    elif len(timeout):
        wiad = "Nie udało się odczytać wartości z czujników "
        for i in range(0, len(timeout)):
            if i == len(timeout) - 1:
                wiad += timeout[i] + ". "
            else:
                wiad += timeout[i] + ", "
        print(wiad)
        send_email("Błąd odczytu temperatury", wiad)
        
    elif len(not_connected):
        wiad = "Nie udało sie połączyć z "
        for i in range(0, len(not_connected)):
            if i == len(not_connected) - 1:
                wiad += not_connected[i] + ". "
            else:
                wiad += not_connected[i] + ", "
        print(wiad)
        send_email("Błąd odczytu temperatury", wiad)


def send_email(subject, content):
    gmailaddress = "zawierzyciel98@gmail.com"
    gmailpassword = "lgoiurgujoebzxfj"

    msg = EmailMessage()
    msg.set_content(content)
    msg['subject'] = subject
    msg['to'] = "strazakdave@gmail.com"
    msg['from'] = gmailaddress

    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.starttls()
    mailServer.login(gmailaddress, gmailpassword)
    mailServer.send_message(msg)
    print("Sent!")
    mailServer.quit()


def check_aqua_all():
    con = sqlite3.connect('db.sqlite3')  # otwarcie bazy danych
    cur = con.cursor()
    for i in cur.execute('SELECT id FROM app_sensor WHERE fun = "aqua"'):
        time_check(i[0]) 
    cur.close()

    
def time_check(_id):
    question = """SELECT fluo_start,fluo_stop,led_start,led_stop,fluo_mode,led_mode,mode FROM app_aqua WHERE sensor_id = ?"""
    resp = aqua_database_settings(question,_id)
    print(resp)
    aqua_ip = get_sensor_ip(_id)[0]
    aqua_port = 7863
    
    
    if datetime.now().hour < 10:
        hours = "0"+str(datetime.now().hour)
    else:
        hours = str(datetime.now().hour)
   
    if datetime.now().minute < 10:
        minutes = ":0"+str(datetime.now().minute)+ ':'+ str(datetime.now().second)
    else:
        minutes = ":"+str(datetime.now().minute)+ ':'+ str(datetime.now().second)
        
    timeNow = hours + minutes
    
    if(resp[6]==0):
        if resp[0]< timeNow and timeNow <=resp[1]:
            if resp[4] == 0:
                message = "s1"
                send_data(message, aqua_ip, aqua_port)
                question = """UPDATE app_aqua SET fluo_mode = 1 WHERE sensor_id = ?"""
                aqua_database_settings(question,_id)   
        else:
            if resp[4] == 1:
                message = "s0"
                send_data(message, aqua_ip, aqua_port)
                question = """UPDATE app_aqua SET fluo_mode = 0 WHERE sensor_id = ?"""
                aqua_database_settings(question,_id) 
                
        if resp[2]< timeNow <=resp[3]:
            if resp[5] == 0:
                message = "r1"
                send_data(message, aqua_ip, aqua_port)
                question = "UPDATE app_aqua SET led_mode = 1 WHERE sensor_id = ?"
                aqua_database_settings(question,_id)
        else:
            if resp[5] == 1:
                message = "r0"
                send_data(message, aqua_ip, aqua_port)
                question = "UPDATE app_aqua SET led_mode = 0 WHERE sensor_id = ?"
                aqua_database_settings(question,_id)
      
                
def aqua_database_settings(_q,_p):
    con = sqlite3.connect('db.sqlite3')  # otwarcie bazy danych
    cur = con.cursor()
    if _q[0] == "S":
        for i in  cur.execute(_q,(_p,)):
            resp = i
        cur.close()
        return resp
    elif _q[0] == "U":
        cur.execute(_q,(_p,))
        con.commit()
        cur.close()
        

def get_sensor_ip(_id):
    ip =[]
    con = sqlite3.connect('db.sqlite3')  # otwarcie bazy danych
    cur = con.cursor()
    for i in cur.execute("SELECT ip FROM app_sensor WHERE id = ? ",(_id,)):
        ip.append(i[0])
    cur.close()
    return ip


def send_data(_mess, _ip, _port):
    try:
        wiad = str.encode(_mess)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # INTERNET / UDP
        sock.sendto(wiad, (_ip, _port))
        sock.close()
    except:
        sock.close()
        return "Nie udało się wysłać"
    
    
minuteOld = datetime.now().minute
hourOld = datetime.now().hour
if __name__ == '__main__':
    # measurement_temp()
    # print("zaczynam")
    # check_aqua_all()
    measurement_temp()
    # while True:
    #     hourNew = datetime.now().hour
    #     minuteNew = datetime.now().minute
    #     if hourOld != hourNew:
    #         hourOld = hourNew
    #         measurement_temp()
        # if minuteOld != minuteNew:
        #     checkAqua()
            
    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # INTERNET / UDP
    # wiad = str.encode("password_temp")
    # sock.sendto(wiad, ("192.168.43.80", 3984))
    # print("wysłano")
    # sock.settimeout(5)
    # data_rec = sock.recvfrom(1024)
    # print(data_rec)
    # temp = data_rec[0].decode("UTF-8")
    # print(temp)
    # sock.close()
    