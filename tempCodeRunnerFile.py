# if __name__ == '__main__':

#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     sock.bind(('', 6785))
#     while(True):
#         data_rec=sock.recvfrom(1024)
#         message=data_rec[0].decode('UTF-8')

#         if message == 'RFID' or message == 'still' or message == 'click':
#             light_lamp(data_rec)
#         else:
#             check_uid(data_rec)
