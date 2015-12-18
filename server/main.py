import socket
import select
from client import Client

def acceptNewConnection(sock):
    rlist, wlist, xlist = select.select([sock], [], [], 0)
    if sock not in rlist:
        return None
    newSocket, addr = sock.accept()
    return Client(newSocket, addr)

def checkDisconnection(clients):
    disconnected = []
    for client in clients:
        if not client.isAlive():
            disconnected.append(client)
    return disconnected

def sendAll(clients, data):
    for client in clients:
        client.send(data)

def checkNewMessage(clients):
    data = []
    rlist, wlist, xlist = select.select([i.sock for i in clients], [], [], 0)
    for client in clients:
        if client.sock in rlist:
            msg = client.receive()
            if msg != None:
                data.append((client, msg))
    return data

HOST = ''
PORT = 1234

listensocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listensocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listensocket.bind((HOST, PORT))
listensocket.setblocking(False)
listensocket.listen(1)

clients = []

while True:
    client = acceptNewConnection(listensocket)
    if client:
        print("A new client connected from:", client.addr[0])
        sendAll(clients, "Yay a new friend! :)")
        clients.append(client)
        client.send("HELLO")
    for client in checkDisconnection(clients):
        print("A client disconnected")
        clients.remove(client)
        sendAll(clients, "Oh no a friend just left :(")
    for client, msg in checkNewMessage(clients):
        print(client.addr, "sent:", msg)
        if msg == "exit":
            break
listensocket.close()
