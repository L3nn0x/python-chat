import socket
import select
from threading import Thread, Event

from common.packet import *
from common.protocol import *

from collections import deque

class   Client(Thread):
    def __init__(self, parent, ip, port):
        super().__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.parent = parent
        self.ip = ip
        self.port = port
        self.connected = True
        self.wpackets = deque()
        self.sent = deque()

    # The callback is called with None if OK, the error message otherwise
    def send(self, packet, callback=None):
        if not self.connected:
            return
        self.wpackets.append((packet, callback))

    def run(self):
        try:
            self.sock.connect((self.ip, self.port))
            self.connected = True
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
                self.sent.append(packet)
            if len(rlist):
                packet = recvPacket(self.sock)
                if not packet:
                    self.stop("Connection closed by remote peer")
                else:
                    self.crunch(packet)

    def crunch(self, packet):
        try:
            if packet.packetType == HELLO:
                p = self.sent.popleft()
            elif packet.packetType == OK:
                p = self.sent.popleft()
                if p and p[1]:
                    p[1](None)
            elif packet.packetType == NOK:
                p = self.sent.popleft()
                if p and p[1]:
                    p[1](packet.get('reason'))
            else:
                self.parent.crunch(packet)
        except Exception as e:
            self.stop("Error: {}".format(e))

    def stop(self, error = ""):
        self.connected = False
        for packet in list(self.wpackets):
            sendPacket(self.sock, self.wpackets.popleft()[0])
        if error:
            print(error)
        self.sock.close()
