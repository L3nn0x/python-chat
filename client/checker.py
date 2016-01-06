from threading import Thread, Event

from client import Client

from common.protocol import *
from common.packet import *

class   Checker(Thread):
    def __init__(self, window):
        super().__init__()
        self.login = Event()
        self.ok = True
        self.window = window
        self.client = None

    def run(self):
        from window import LoginState
        loginstate = LoginState(self.window, self)
        self.window.states.push(loginstate)
        while self.ok:
            self.login.wait()
            self.login.clear()
            try:
                tmp = self._login
            except AttributeError:
                break
            if self.client:
                self.client.stop()
                self.client.join()
            self.client = Client(self, "127.0.0.1", 1234, self._login, self._password)
            self.client.start()
            self.client.update.wait()
            self.client.update.clear()
            if len(self.client.error):
                if not self.ok:
                    break
                loginstate.error.set(self.client.error)
            else:
                self.window.states.pop()
                self.client.update.wait()
                if not self.ok:
                    break
                loginstate = LoginState(self.window, self)
                self.window.states.push(loginstate)

    def stop(self):
        self.ok = False
        self.login.set()
        if self.client:
            self.client.update.set()
            self.client.stop()
            self.client.join()

    def sendMsg(self, data):
        if not len(data):
            return
        callback = self.window.getChannel("general").addMessage(self._login, data)
        self.client.send(msg(self._login, 'general', data), callback)

    def crunch(self, packet):
        if packet.packetType == MSG:
            self.window.getChannel(packet.get('destination')).getMessage(packet.get('source'), packet.get('data'), packet.get('id'))
        elif packet.packetType == HISTORY:
            for name, history in packet.kwargs.items():
                self.window.getChannel(name).setHistory(history)
        else:
            print(packet)
