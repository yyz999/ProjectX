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
s.connect(('localhost', sys.argv[1]))


# HTTPRequestHandler class
class CtlHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        if self.path == '/':
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

    def do_POST(self):
        # check cmd
        global msg
        global last_cmd_timestamp
        global enable
        global s
        request_headers = self.headers
        content_length = request_headers.get('Content-Length')
        content = self.rfile.read(int(content_length))
        self.send_response(200)

        items = str(content).split('\'')[1].split('/')
        msg = '%s:%s:%s' % (items[0], items[1], items[2])
        items = msg.split(':')
        if len(items) != 3:
            return
        if items[0] != 'M':
            return
        if int(items[1]) > 127 or int(items[1]) < 0:
            return
        if int(items[2]) > 127 or int(items[2]) < 0:
            return
        self.send_response(200)
        s.sendall(msg)


def run():
    # socket started
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('localhost', 8888)
    httpd = HTTPServer(server_address, CtlHTTPServer_RequestHandler)
    print('running server...')
    httpd.serve_forever()


# Main()
run()