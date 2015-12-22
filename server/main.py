import socket
from client import Client
from server import Server

listensocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listensocket.bind(('', 1234))
listensocket.listen(1)

server = Server()

print("starting")
while True:
    try:
        sock, addr = listensocket.accept()
        server.newClient(sock, addr)
    except KeyboardInterrupt:
        break

print("closing")
server.close()

listensocket.close()
