import os
import django
import socket

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smart_home.settings")

django.setup()

from rpl.mod import check_lamp, check_uid


def listener() -> None:
    """
    This function receives commands from microcontrollers.
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", 6785))
    while True:
        try:
            data_rec = sock.recvfrom(1024)
            message = data_rec[0].decode("UTF-8")
            if message:
                match message:
                    case "still" | "click" | "RFID":
                        ip: str = data_rec[1][0]
                        check_lamp(message, ip)
                    case _:
                        try:
                            UID = int(message)
                            if type(UID) == int:
                                uid: str = message
                                ip: str = data_rec[1][0]
                                port: str = data_rec[1][1]
                                check_uid(uid, ip, port)
                        except Exception as e:
                            pass
        except Exception as e:
            pass


if __name__ == "__main__":
    listener()
