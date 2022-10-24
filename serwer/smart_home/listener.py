import sqlite3
import socket


def checkUID(data):
    try:
        con = sqlite3.connect('db.sqlite3')
        cur = con.cursor()
        id = cur.execute("SELECT id FROM app_sensor WHERE ip = ?",(data[1][0],))
        for uid in cur.execute("SELECT uid FROM app_card WHERE sensor_id = ?",(id.fetchone()[0],)):
            if(uid[0] == int(data[0].decode('UTF-8'))):
                sock.sendto(str.encode('access'), data[1])
                break
        else:
            sock.sendto(str.encode('access-denied'), data[1])
    except Exception as e:
        print(e)
        
def lightLamp(data,sensor):
    con = sqlite3.connect('smart_home/db.sqlite3')
    cur = con.cursor()
    id = cur.execute("SELECT id FROM app_sensor WHERE ip = ?",(data[1][0],)).fetchone()[0]
    if data_rec[0].decode('UTF-8') == 'RFID':
        ip = cur.execute("SELECT lamp FROM app_rfid WHERE sensor_id = ?",(id,)).fetchone()[0]
    elif data_rec[0].decode('UTF-8') == 'still' or data_rec[0].decode('UTF-8') == 'click':
        ip = cur.execute("SELECT lamp FROM app_button WHERE sensor_id = ?",(id,)).fetchone()[0]
        
    print(ip)
    if ip != "":
        print(ip)
        sock.sendto(str.encode(data_rec[0].decode('UTF-8')), (ip,4569))
        print("wysyłam wiadomość {}".format(data_rec[0].decode('UTF-8')))
    print('tu')

if __name__ == '__main__':
    ip = str(socket.gethostbyname(socket.gethostname()))
    print(ip)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # INTERNET / UDP
    sock.bind(('', 6785))
    while(True):
        data_rec = sock.recvfrom(1024)
        print(data_rec[0].decode('UTF-8'))
        if data_rec[0].decode('UTF-8') == 'RFID':
            lightLamp(data_rec,"app_rfid")
        if data_rec[0].decode('UTF-8') == 'still' or data_rec[0].decode('UTF-8') == 'click':
            lightLamp(data_rec,"app_button")
        else:
            checkUID(data_rec)






