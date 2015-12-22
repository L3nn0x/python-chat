import socket
from client import Client

listensocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listensocket.bind(('', 1234))
listensocket.listen(1)

clients = []

print("starting")
while True:
    try:
        sock, addr = listensocket.accept()
        clients.append(Client(sock, addr))
        print("a new client connected from:", addr)
        clients[-1].start()
    except KeyboardInterrupt:
        break

print("closing")
for client in clients:
    client.stop()
    client.join()

listensocket.close()
