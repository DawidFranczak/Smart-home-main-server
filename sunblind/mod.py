import socket


def send_data(_mess, _ip, _port) -> bool:
    '''
    Send message to microcontroler on _port and _ip  and waiting for response
    '''
    try:
        wiad = str.encode(_mess)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(wiad, (_ip, _port))
        sock.settimeout(0.5)
        sock.recvfrom(128)
        sock.close()
        return True
    except:
        sock.close()
        return False
