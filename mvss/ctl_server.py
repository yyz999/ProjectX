#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import socket  #for sockets
import sys  #for exit
import threading
import time
from time import sleep


# HTTPRequestHandler class
class CtlHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        f = open('client.html')  #open requested file
        #send code 200 response
        self.send_response(200)
        #send header first
        self.send_header('Content-type', 'text-html')
        self.end_headers()
        #send file content to client
        self.wfile.write(bytes(f.read(), "utf8"))
        f.close()
        return


def SendCallback():
    global s
    global msg
    global enable
    if msg:
        s.sendall(msg)
    else:
        sleep(1)
    if enable:
        threading.Timer(0.1, SendCallback).start()


def run():
    # socket started
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('127.0.0.1', 8888)
    httpd = HTTPServer(server_address, CtlHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()


# Main()
# Init socket
try:
    #create an AF_INET, STREAM socket (TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(
        msg[0]) + ' , Error message : ' + msg[1]
    sys.exit()
s.connect(('localhost', sys.argv[1]))
msg = ''
enable = True
print 'Socket Created'
threading.Timer(1, SendCallback).start()
run()