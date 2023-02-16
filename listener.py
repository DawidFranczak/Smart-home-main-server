import sqlite3
import socket


def check_uid(data):
    ''' Check incoming uid from RFID sensor '''
    try:
        con = sqlite3.connect('db.sqlite3')
        cur = con.cursor()
        
        sensor_ip=data[1][0]
        sensor_uid=int(data[0].decode('UTF-8'))
        
        id = cur.execute("SELECT id FROM app_sensor WHERE ip = ?",(sensor_ip,))
        for uid in cur.execute("SELECT uid FROM app_card WHERE sensor_id = ?",(id.fetchone()[0],)):
            if(uid[0]==sensor_uid ):
                sock.sendto(str.encode('access'), data[1])
                break
        else:
            sock.sendto(str.encode('access-denied'), data[1])
    except Exception as e:
        print(e)
        
def light_lamp(data):
    ''' Check connected lamp to rfid sensor and button and turn it on '''
    
    con = sqlite3.connect('smart_home/db.sqlite3')
    cur = con.cursor()
    
    sensor_id = data[1][0]
    message = data_rec[0].decode('UTF-8')
    
    id = cur.execute("SELECT id FROM app_sensor WHERE ip = ?",(sensor_id,)).fetchone()[0]
    if message == 'RFID':
        ip = cur.execute("SELECT lamp FROM app_rfid WHERE sensor_id = ?",(id,)).fetchone()[0]
    elif message == 'still' or message == 'click':
        ip = cur.execute("SELECT lamp FROM app_button WHERE sensor_id = ?",(id,)).fetchone()[0]
        
    if ip != "":
        sock.sendto(str.encode(data_rec[0].decode('UTF-8')), (ip,4569))
        print("wysyłam wiadomość {}".format(data_rec[0].decode('UTF-8')))


ip = str(socket.gethostbyname(socket.gethostname()))
print(ip)

if __name__ == '__main__':

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 6785))
    while(True):
        data_rec=sock.recvfrom(1024)
        message=data_rec[0].decode('UTF-8')
        
        if message == 'RFID' or message == 'still' or message == 'click':
            light_lamp(data_rec)
        else:
            check_uid(data_rec)



