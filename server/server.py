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

    def checkUser(self, login, password):
        return login == 'user'

    def checkAlive(self):
        for client in self.clients[:]:
            if not client.connected or not client.isAlive():
                if client.isAlive():
                    client.stop()
                    client.join()
                self.clients.remove(client)

    def close(self):
        for client in self.clients:
            print(client.login)
            client.stop()
            client.join()

    def getProfiles(self):
        p = {}
        for c in self.clients:
            if not c.login:
                continue
            p[c.login] = c.profile
        return p

    def getChannelNames(self, channel):
        names = []
        for client in self.clients:
            if client.login and channel in client.chans:
                names.append(client.login)
        return names

    def getChannelHistory(self, channel):
        return self.channels[channel].getHistory()
    
    def send(self, login, packet):
        self.lock.acquire()
        for client in self.clients:
            if client.login == login:
                client.send(packet)
        self.lock.release()
    
    def sendChannel(self, channel, packet):
        self.lock.acquire()
        id = self.channels[channel].addMessage(
                packet.get('source'), packet.get('data'))
        packet.append(id=id)
        for client in self.clients:
            if channel in client.chans:
                client.send(packet)
        self.lock.release()

    def sendAll(self, packet):
        self.lock.acquire()
        for client in self.clients:
            client.send(packet)
        self.lock.release()

    def sendAllExcept(self, client, packet):
        self.lock.acquire()
        for c in self.clients:
            if c.login == client:
                continue
            c.send(packet)
        self.lock.release()
