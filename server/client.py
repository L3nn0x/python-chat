from threading import Thread
import select
from common.packet import *
from common.protocol import *
from collections import deque

class   Client(Thread):
    _CONNECT = 0
    _LOGIN = 1
    _NORMAL = 2
    def __init__(self, sock, addr):
        super().__init__()
        self.sock = sock
        self.addr = addr
        self.chans = ['general']
        self.connected = True
        self.state = Client._CONNECT
        self.states = {
                Client._CONNECT: self.connect,
                Client._LOGIN: self.login,
                Client._NORMAL: self.normal,
            }
        self.wpackets = deque()

    def run(self):
        while self.connected:
            rlist, wlist, xlist = select.select([self.sock], [self.sock], [])
            if len(rlist):
                packet = recvPacket(self.sock)
                if not packet:
                    self.stop()
                else:
                    print("Client", self.addr, "sent:")
                    print(packet)
                    self.crunch(packet)
            elif len(wlist) and len(self.wpackets):
                if not sendPacket(self.sock, self.wpackets.popleft()):
                    self.stop()

    def send(self, packet):
        self.wpackets.append(packet)

    def crunch(self, packet):
        try:
            self.states[self.state](packet)
        except Exception as e:
            print("Unknown error:", e)
            self.stop()

    def connect(self, packet):
        if packet.packetType != HELLO:
            self.stop()
            return
        self.send(hello())
    
    def login(self, packet):
        pass

    def normal(self, packet):
        pass

    def stop(self):
        print("Client disconnected:", self.addr)
        self.connected = False
        self.sock.close()
