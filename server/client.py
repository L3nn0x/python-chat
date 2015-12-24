from threading import Thread
import select
from common.packet import *
from common.protocol import *
from collections import deque

class   Client(Thread):
    _CONNECT = 0
    _LOGIN = 1
    _NORMAL = 2
    def __init__(self, parent, sock, addr):
        super().__init__()
        self.sock = sock
        self.addr = addr
        self.chans = ['general']
        self.connected = True
        self.parent = parent
        self.state = Client._CONNECT
        self.states = {
                Client._CONNECT: self.connect,
                Client._LOGIN: self.login,
                Client._NORMAL: self.normal,
            }
        self.wpackets = deque()
        self.login = None
        self.profile = None

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
        if not self.connected:
            return
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
        self.state = Client._LOGIN
    
    def login(self, packet):
        if packet.packetType != CREDENTIALS:
            self.stop()
            return
        if packet.get('password') == 'test':
            self.login = packet.get('login')
            self.send(ok())
            self.profile = {
                    "nick": "Little pony",
                    "status": "active",
                    }
            p = Packet(PROFILE)
            p.kwargs[self.login] = self.profile
            self.send(p)
            chans = {}
            for chan in self.chans:
                chans[chan] = self.parent.getChannelNames(chan)
            self.send(channels(**chans))
            self.state = Client._NORMAL
        else:
            self.send(nok("login or password mismatched"))

    def normal(self, packet):
        if packet.packetType == MSG:
            if packet.get('destination') not in self.chans:
                self.send(nok("This channel doesn't exist!"))
                return
            self.send(ok())
            self.parent.sendChannel(packet.get('destination'), packet)

    def stop(self):
        if not self.connected:
            return
        self.connected = False
        for packet in list(self.wpackets):
            print("sending")
            sendPacket(self.sock, self.wpackets.popleft())
        print("Client disconnected:", self.addr)
        self.sock.close()
