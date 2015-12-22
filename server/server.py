from client import Client

class   Server:
    def __init__(self):
        self.clients = []

    def newClient(self, sock, addr):
        self.clients.append(Client(self, sock, addr))
        print("A new client connected:", addr)
        self.clients[-1].start()

    def close(self):
        for client in self.clients:
            client.stop()
            client.join()
    
    def send(self, login, packet):
        for client in self.clients:
            if client.login == login:
                client.send(packet)
    
    def sendChannel(self, channel, packet):
        for client in self.clients:
            if channel in client.chans and client.login:
                client.send(packet)

    def sendAll(self, packet):
        for client in self.clients:
            if client.login:
                client.send(packet)
