import socket
import select
from threading import Thread

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
        self.sent = False
        self.error = ""
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
            self.sent = False
            self.state += 1

    def credentials(self, packet):
        if packet.packetType == NOK:
            self.error = packet.reason
        elif packet.packetType == OK:
            self.loggued = True
            self.sent = False
            self.state += 1
        else:
            self.stop("Error of protocol: {}".format(packet))

    def send(self, packet):
        if not self.connected:
            return
        self.wpackets.append(packet)

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
            if len(wlist) and len(self.wpackets) and not self.sent:
                if not sendPacket(self.sock, self.wpackets.popleft()):
                    self.stop("Error while sending a packet")
                self.sent = True
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
                    self.sent = False
                elif packet.packetType == NOK:
                    self.error = packet.get('reason')
                else:
                    self.parent.crunch(packet)
        except Exception as e:
            self.stop("Error: {}".format(e))

    def stop(self, error = ""):
        self.connected = False
        for packet in list(self.wpackets):
            sendPacket(self.sock, self.wpackets.popleft())
        self.error = error
        if error:
            print(error)
        self.sock.close()
