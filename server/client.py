import select
import socket
from threading import Thread
from common.packets import send, SIZE
from common.protocol import *

class   NoDataException(Exception):
    pass

class   Client(Thread):
    _CONNECTED = 0
    _LOGIN = 1
    _NORMAL = 3

    def __init__(self, parent, socket, addr):
        super().__init__()
        self.sock = socket
        self.addr = addr
        self.connected = True
        self._nick = None
        self.channels = ["general"]
        self.parent = parent
        self.state = Client._CONNECTED
        self.states = {
                Client._CONNECTED: self.connection,
                Client._LOGIN: self.login,
                Client._NORMAL: self.crunch,
                }

    def run(self):
        while self.connected:
            try:
                if not self.treat(self.getData()):
                    self.stop()
            except NoDataException:
                self.stop()

    def getData(self, size = SIZE):
        data = None
        while not data:
            rlist, wlist, xlist = select.select([self.sock], [], [], 1)
            if not self.isAlive():
                raise NoDataException()
            elif self.sock in rlist:
                data = self.sock.recv(size)
                if not data:
                    raise NoDataException()
        return data

    def treat(self, data):
        from common.utils import atoi
        size = atoi(data.decode("latin1"))
        if size <= 1:
            return False
        data = data[len(str(size)):]
        while len(data) < size:
            tmp = self.getData(size - len(data))
            if tmp is None and len(data) < size:
                return False
            else:
                data += tmp
        return self.states[self.state](data[:size])

    def connection(self, data):
        data = data.decode("latin1")
        if data != HELLO:
            return False
        if self.parent.maintenance:
            self.send(NOK)
            self.stop()
        else:
            self.send(HELLO)
        self.state = Client._LOGIN
        return True

    def login(self, data):
        data = data.decode("latin1")
        data = data.split(' ')
        if data[0] != CREDENTIALS:
            return False
        self.login = data[1]
        if self._nick == None:
            self._nick = self.login
        self.send(OK)
        for chan in self.channels:
            self.send(protFormat(CHAN, chan))
        self.send(OK)
        self.state = Client._NORMAL
        return True

    def crunch(self, data):
        data = data.decode("latin1")
        data = data.split(' ')
        dic = {
                SEND_MSG: self.msg,
            }
        try:
            dic[data[0]](data[1:])
        except KeyError:
            pass
        return True

    def msg(self, data):
        if data[0] not in self.channels:
            self.send(NOK)
            return True
        self.parent.sendChannel(self, data[0], ' '.join(data[1:]))
        return True

    def send(self, data, encode = True):
        send(self.sock, data, encode)

    def stop(self):
        if not self.connected:
            return
        self.send(END)
        self.connected = False
        self.sock.close()

    def isAlive(self):
        if self.connected:
            self.sock.sendall("".encode())
        else:
            return False
        return True


