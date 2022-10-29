   # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # INTERNET / UDP
    # sock.bind(('', 6785))
    # while(True):
    #     data_rec = sock.recvfrom(1024)
    #     print(data_rec[0].decode('UTF-8'))
    #     if data_rec[0].decode('UTF-8') == 'RFID':
    #         lightLamp(data_rec,"app_rfid")
    #     if data_rec[0].decode('UTF-8') == 'still' or data_rec[0].decode('UTF-8') == 'click':
    #         lightLamp(data_rec,"app_button")
    #     else:
    #         checkUID(data_rec)