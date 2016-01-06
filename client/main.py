from client import Client
from window import MainWindow, LOGIN, CHANNEL
from common.protocol import *
from threading import Event

class   Cruncher:
    def __init__(self, window):
        self.window = window
        self.window.register(self.update)
        self.window.registerAlive(self.isAlive)
        self.client = Client(self, "127.0.0.1", 1234)
        self.client.start()
        self.client.send(hello())
        self.login = None
        self.packets = {
                HISTORY: self.history,
                MSG: self.msg,
            }

    def isAlive(self):
        if not self.client.isAlive():
            self.client = Client(self, "127.0.0.1", 1234)
            self.client.start()
            self.client.send(hello())
            self.window.cleanStates()

    def update(self, data):
        if data[0] == LOGIN:
            data = data[1:]
            self.client.send(credentials(data[0], data[1]), data[2])
            self.login = data[0]
        elif data[0] == CHANNEL:
            data = data[1:]
            c = self.window.getChannel(data[0]).addMessage(self.login, data[1])
            self.client.send(msg(self.login, data[0], data[1]), c)

    def stop(self):
        self.client.stop()
        self.client.join()

    def history(self, packet):
        for name, his in packet.kwargs.items():
            channel = self.window.getChannel(name)
            channel.setHistory(his)
        if 'general' in packet.kwargs:
            self.window.selectChannel('general')

    def msg(self, packet):
        channel = self.window.getChannel(packet.get('destination'))
        channel.getMessage(packet.get('source'), packet.get('data'), packet.get('id'))

    def crunch(self, packet):
        try:
            self.packets[packet.packetType](packet)
        except KeyError:
            print(packet)

window = MainWindow()
cruncher = Cruncher(window)
window.mainloop()
cruncher.stop()
