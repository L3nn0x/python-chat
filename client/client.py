import socket
import select
from threading import Thread, Event

from common.packet import *
from common.protocol import *

from collections import deque

class   Client(Thread):
    _HELLO = 0
    _CREDENTIALS = 1
    _NORMAL = 2
    def __init__(self, parent, ip, port, login, password):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.parent = parent
        self.ip = ip
        self.port = port
        self.connected = True
        self.login = login
        self.password = password
        self.wpackets = deque()
        self.state = Client._HELLO
        self.loggued = False
        self.sent = deque()
        self.error = ""
        self.update = Event()
        self.states = [
                self.hello,
                self.credentials
            ]
        self.send(hello())

    def hello(self, packet):
        if packet.packetType != HELLO:
            self.stop("Error of protocol: {}".format(packet))
        else:
            self.send(credentials(self.login, self.password))
            self.state += 1

    def credentials(self, packet):
        if packet.packetType == NOK:
            self.error = packet.get('reason')
            self.update.set()
        elif packet.packetType == OK:
            self.loggued = True
            self.update.set()
            self.state += 1
        else:
            self.stop("Error of protocol: {}".format(packet))

    # call it with None or the error message
    def send(self, packet, callback=None):
        if not self.connected:
            return
        self.wpackets.append((packet, callback))

    def run(self):
        try:
            self.sock.connect((self.ip, self.port))
        except Exception as e:
            self.stop("Error while connecting: {}".format(e))
        while self.connected:
            write = []
            if len(self.wpackets):
                write = [self.sock]
            rlist, wlist, xlist = select.select([self.sock], write, [self.sock], 0.2)
            if len(xlist):
                self.stop("Error with the socket")
            if len(wlist) and len(self.wpackets):
                packet = self.wpackets.popleft()
                if not sendPacket(self.sock, packet[0]):
                    self.stop("Error while sending a packet")
                    break
                if self.state >= len(self.states):
                    self.sent.append(packet)
                self.error = ""
            if len(rlist):
                packet = recvPacket(self.sock)
                if not packet:
                    self.stop("Connection closed by remote peer")
                else:
                    self.crunch(packet)

    def crunch(self, packet):
        try:
            if self.state < len(self.states):
                self.states[self.state](packet)
            else:
                if packet.packetType == OK:
                    p = self.sent.popleft()
                    if p and p[1]:
                        p[1](None)
                elif packet.packetType == NOK:
                    p = self.sent.popleft()
                    self.error = packet.get('reason')
                    if p and p[1]:
                        p[1](self.error)
                else:
                    self.parent.crunch(packet)
        except Exception as e:
            self.stop("Error: {}".format(e))

    def stop(self, error = ""):
        self.connected = False
        for packet in list(self.wpackets):
            sendPacket(self.sock, self.wpackets.popleft()[0])
        self.error = error
        self.update.set()
        if error:
            print(error)
        self.sock.close()
