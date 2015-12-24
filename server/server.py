from client import Client
from message import Channel
from collections import defaultdict
from threading import Lock

class   Server:
    def __init__(self):
        self.clients = []
        self.channels = defaultdict(Channel)
        self.lock = Lock()

    def newClient(self, sock, addr):
        self.clients.append(Client(self, sock, addr))
        print("A new client connected:", addr)
        self.clients[-1].start()

    def close(self):
        for client in self.clients:
            client.stop()
            client.join()

    def getChannelNames(self, channel):
        names = []
        for client in self.clients:
            if client.login and channel in client.chans:
                names.append(client.login)
        return names
    
    def send(self, login, packet):
        for client in self.clients:
            if client.login == login:
                client.send(packet)
    
    def sendChannel(self, channel, packet):
        self.lock.acquire()
        id = self.channels[channel].addMessage(
                packet.get('source'), packet.get('data'))
        packet.append(id=id)
        for client in self.clients:
            if channel in client.chans and client.login:
                client.send(packet)
        self.lock.release()

    def sendAll(self, packet):
        for client in self.clients:
            if client.login:
                client.send(packet)
