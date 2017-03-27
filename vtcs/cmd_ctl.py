import socket  #for sockets
import sys  #for exit
import threading
import time

try:
    #create an AF_INET, STREAM socket (TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(
        msg[0]) + ' , Error message : ' + msg[1]
    sys.exit()
msg = ''
enable = True


def SendCallback():
    global s
    global msg
    global enable
    s.sendall(msg)
    if enable:
        threading.Timer(0.2, SendCallback).start()


print 'Socket Created'
threading.Timer(1, SendCallback).start()
host = sys.argv[1]
port = int(sys.argv[2])
#Connect to remote server
s.connect((host, port))
while True:
    message = raw_input('mag dir | exit\n')
    if message == 'exit':
        break
    msg = message
enable = False
time.sleep(1)
s.close()