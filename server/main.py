import time
import select
import socket
# from client import Client
from common.protocol import *
from common.packets import *

parent = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
parent.bind(('', 1234))
parent.listen(1)
sock, addr = parent.accept()

s = Socket(sock, addr)

s.sendData(send(createPacket(CHAN, [1 for i in range(SIZE+10)]), True))
s.sendData(send(createPacket(CHAN, "plop")))
s.sendData(send(createPacket(HELLO)))

t = time.time()
while time.time() - t < 15:
    s.update(1)

sock.close()
parent.close()

# class   Server:
#     def __init__(self):
#         self.clients = []
#         self.maintenance = False

#     def addClient(self, sock, addr):
#         self.clients.append(Client(self, sock, addr))
#         self.clients[-1].start()

#     def removeClient(self, client):
#         client.stop()
#         client.join()
#         self.clients.remove(client)

#     def checkAlive(self):
#         for client in self.clients[:]:
#             if not client.connected:
#                 self.removeClient(client)
#                 print("A client disconnected")

#     def close(self):
#         for client in self.clients:
#             client.stop()
#             client.join()

#     def sendall(self, data, encode = True):
#         for client in self.clients:
#             if client._nick:
#                 client.send(data, encode)

#     def sendallexcept(self, _client, data, encode = True):
#         for client in self.clients:
#             if client != _client and client._nick:
#                 client.send(data, encode)

#     def sendChannel(self, client, channel, data):
#         for client in self.clients:
#             if channel in client.channels:
#                 client.send(protFormat(MSG, client.login, channel, data))

# listensocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# listensocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# listensocket.bind(('', 1234))
# listensocket.setblocking(False)
# listensocket.listen(1)

# server = Server()

# print("Launching")
# try:
#     while True:
#         rlist, wlist, xlist = select.select([listensocket], [], [], 1)
#         if listensocket in rlist:
#             sock, addr = listensocket.accept()
#             print("A new client connected")
#             server.addClient(sock, addr)
#         server.checkAlive()
# except:
#     pass

# print("Terminating")
# server.close()
