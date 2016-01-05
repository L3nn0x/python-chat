import socket
import select
from common.protocol import *
from common.packet import *

from client import Client

from window import MainWindow

class   Parent:
    def __init__(self, window, login, passwd):
        self.client = Client(self, "127.0.0.1", 1234, login, passwd)
        self.login = login
        self.window = window
        self.client.start()

    def stop(self):
        self.client.stop()
        self.client.join()

    def sendMsg(self, data):
        if not len(data):
            return
        callback = self.window.channel.addMessage(self.login, data)
        self.client.send(msg(self.login, 'general', data), callback)

    def crunch(self, packet):
        if packet.packetType == MSG:
            self.window.channel.getMessage(packet.get('source'), packet.get('data'), packet.get('id'))
        print(packet)

window = MainWindow()
parent = Parent(window, "user", "test")
window.bind(parent.sendMsg)
window.mainloop()
parent.stop()
