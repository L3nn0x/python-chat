from threading import Thread
import select
from common.packet import *

class   Client(Thread):
    def __init__(self, sock, addr):
        super().__init__()
        self.sock = sock
        self.addr = addr
        self.connected = True

    def run(self):
        while self.connected:
            rlist = select.select([self.sock], [], [], 1)[0]
            if len(rlist):
                packet = recvPacket(self.sock)
                if not packet:
                    self.stop()
                else:
                    print(packet)

    def stop(self):
        self.connected = False
        self.sock.close()
