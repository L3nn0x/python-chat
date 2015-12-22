import socket
import select
from common.packet import *

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 1234))
a = Packet("test", "test")
print(a)
sendPacket(sock, a)
sock.close()
