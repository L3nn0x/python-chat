import socket
import time
from common.packets import *

class   Client:
    def __init__(self, sock, addr):
        self.sock = sock
        self.sock.setblocking(False)
        self.addr = addr
        self.lastCheck = time.time()
        self.buffer = ""
        self.size = ""

    def __del__(self):
        self.sock.close()

    def send(self, data):
        try:
            send(self.sock, data)
        except socket.error:
            return False
        return True

    def receive(self):
        return receive(self.sock)

    def isAlive(self):
        ret = True
        if time.time() - self.lastCheck > 5.0:
            ret = self.send("")
            self.lastCheck = time.time()
        return ret
