#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import socket  #for sockets
import sys  #for exit
import threading
import time
from time import sleep

msg = ''
last_cmd_timestamp = time.time()
# Init socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect(('localhost', sys.argv[1]))
enable = True
print('Socket Created')


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

    def do_CMD(self):
        # check cmd
        global msg
        global last_cmd_timestamp
        global enable
        print(self.path)
        items = self.path.split(':')
        if len(items) != 3:
            return
        if items[0] != 'M':
            return
        if int(item[1]) > 127 or int(item[1]) < 0:
            return
        if int(item[2]) > 127 or int(item[2]) < 0:
            return
        msg = self.path
        last_cmd_timestamp = time.time()
        self.send_response(200)
        self.send_header("content-type", "text-html")
        self.end_headers()
        self.wfile.write(bytes('Done', "utf8"))
        if not enable:
            enable = True
            threading.Timer(0.1, SendCallback).start()


def SendCallback():
    global s
    global msg
    global enable
    global last_cmd_timestamp
    if msg:
        #s.sendall(msg)
        print('send msg=' + msg)
    else:
        sleep(1)
    if time.time() - last_cmd_timestamp > 1:
        enable = False
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
threading.Timer(1, SendCallback).start()
run()