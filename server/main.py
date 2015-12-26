import socket
from client import Client
from server import Server

listensocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listensocket.settimeout(0.2)
listensocket.bind(('', 1234))
listensocket.listen(2)

server = Server()

print("starting")
while True:
    try:
        try:
            sock, addr = listensocket.accept()
        except socket.timeout:
            server.checkAlive()
            continue
        server.newClient(sock, addr)
    except KeyboardInterrupt:
        break

print("closing")
server.close()

listensocket.close()
