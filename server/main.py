import socket
import select
from common.packets import *

class   Client:
    def __init__(self, socket, addr):
        self.socket = socket
        self.addr = addr

    def send(self, data):
        send(self.socket, data)

    def receive(self):
        return receive(self.socket)

HOST = ''
PORT = 1234

listensocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listensocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listensocket.bind((HOST, PORT))
listensocket.listen(1)

socket, addr = listensocket.accept()
print("connection")
client = Client(socket, addr)
client.send("HELLO")
print(client.receive())
listensocket.close()
