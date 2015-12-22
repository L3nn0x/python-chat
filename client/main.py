import socket
import select
from common.packet import *

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 1234))
a = Packet("test", [i for i in range(256*10)])
print(a)
print(sendPacket(sock, a))
sock.close()
