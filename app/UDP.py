import socket


def send_data(message: str, ip: str, port: int) -> bool:
    """
    This function sends message to the microcontroller.

    :params message: This is command for the microcontroller.
    :params ip: This is microcontroller's ip.
    :params port: This is microcontroller port

    :return: True if communication with microcontroller successfully
    """
    try:
        wiad = str.encode(message)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(wiad, (ip, port))
        sock.settimeout(0.5)
        sock.recvfrom(128)
        sock.close()
        return True
    except TimeoutError:
        sock.close()
        return False
