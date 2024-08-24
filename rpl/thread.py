import socket
import threading
import time

from .mod import check_lamp, check_uid


def listener() -> None:
    """
    This function receives commands from microcontrollers.
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", 6785))
    local_address = sock.getsockname()

    while True:
        try:
            sock.settimeout(0.5)
            data_rec = sock.recvfrom(1024)
            message = data_rec[0].decode("UTF-8")
            print(message)
            if message:
                match message:
                    case "still" | "click" | "RFID":
                        message: str = message[0].decode("UTF-8")
                        ip: str = message[1][0]
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
                            print(f"Złapany wyjątek: {type(e).__name__}")
                            print(f"Szczegóły wyjątku: {e}")
                            print("Unrecognized command.")
        except:
            if not threading.main_thread().is_alive():
                sock.close()
                break
