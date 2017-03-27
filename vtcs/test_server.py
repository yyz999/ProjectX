import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port_number = sys.argv[1]
server_address = ('localhost', port_number)
self.sock.bind(server_address)
self.sock.listen(1)
while True:
    print('Wait for a connection')
    connection, client_address = self.sock.accept()
    try:
        print >> sys.stderr, 'connection from', client_address
        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(32)
            print >> sys.stderr, 'received "%s"' % data
    finally:
        # Clean up the connection
        print('Connection closed')
        connection.close()
