import socket
import select
from common.protocol import *
from common.packet import *

from client import Client

class   Parent:
    def __init__(self):
        self.client = Client(self, "127.0.0.1", 1234, "user", "test")
        self.client.start()
        self.msgs = 0

    def stop(self):
        self.client.stop()
        self.client.join()

    def sendMsg(self, data):
        if not len(data):
            return
        print("sending...")
        self.msgs += 1
        self.client.send(msg(self.client.login, 'general', data))

    def crunch(self, packet):
        print(packet)

    def update(self):
        if self.msgs and not self.client.sent:
            print("sent")
            self.msgs -= 1
        if len(self.client.error):
            print(self.client.error)
            self.client.error = ""

parent = Parent()

while True:
    try:
        rlist = select.select([0], [], [], 0.2)[0]
        if len(rlist):
            data = input()
            parent.sendMsg(data)
            print("#general >", end='', flush=True)
        parent.update()
    except Exception as e:
        print("Exception:", e)
        break
    except KeyboardInterrupt:
        break

parent.stop()
