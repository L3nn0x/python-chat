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
        self.profile = {
                'status': 'active',
                'nick': 'Little pony',
        }

    def run(self):
        while self.connected:
            write = []
            if len(self.wpackets):
                write = [self.sock]
            rlist, wlist, xlist = select.select([self.sock], write, [self.sock], 0.2)
            if len(xlist):
                self.stop("Error with the socket")
            if len(rlist):
                packet = recvPacket(self.sock)
                if not packet:
                    self.stop("Connection closed by remote peer")
                else:
                    print("Client", self.addr, "sent:")
                    print(packet)
                    self.crunch(packet)
            if len(wlist) and len(self.wpackets):
                if not sendPacket(self.sock, self.wpackets.popleft()):
                    self.stop("Error while sending a packet")

    def send(self, packet):
        if not self.connected:
            return
        if packet.packetType not in (HELLO, NOK) and not self.login:
            return
        self.wpackets.append(packet)

    def crunch(self, packet):
        try:
            self.states[self.state](packet)
        except Exception as e:
            self.stop("Unknown error: {}".format(e))

    def connect(self, packet):
        if packet.packetType != HELLO:
            self.stop("Error of protocol: {}".format(packet))
            return
        self.send(hello())
        self.state = Client._LOGIN
    
    def login(self, packet):
        if packet.packetType != CREDENTIALS:
            self.stop("Error of protocol: {}".format(packet))
            return
        if self.parent.checkUser(packet.get('login'), packet.get('password')):
            self.login = packet.get('login')
            self.send(ok())
            self.send(profile(**self.parent.getProfiles()))
            self.parent.sendAllExcept(self.login, profile(**{self.login:self.profile}))
            chans = {}
            for chan in self.chans:
                chans[chan] = self.parent.getChannelNames(chan)
            self.send(channels(**chans))
            chans = {}
            for chan in self.chans:
                chans[chan] = self.parent.getChannelHistory(chan)
            self.send(history(**chans))
            self.state = Client._NORMAL
        else:
            self.send(nok("login or password mismatched"))

    def normal(self, packet):
        if packet.packetType == MSG:
            if packet.get('destination') not in self.chans:
                self.send(nok("This channel doesn't exist!"))
                return
            elif packet.get('source') != self.login:
                self.send(nok("You can't send messages as another person"))
                return
            self.send(ok())
            self.parent.sendChannel(packet.get('destination'), packet)

    def stop(self, error = ""):
        if not self.connected:
            return
        self.connected = False
        for packet in list(self.wpackets):
            sendPacket(self.sock, self.wpackets.popleft())
        print("Client disconnected:", self.addr)
        if len(error):
            print(error)
        if self.login:
            self.profile['status'] = "away"
            self.parent.sendAllExcept(self.login, profile(**{self.login:self.profile}))
        self.sock.close()
