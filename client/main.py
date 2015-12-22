import socket
import select
from common.protocol import *
from common.packet import *

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 1234))
print(sendPacket(sock, Packet("plop")))
print(sendPacket(sock, hello()))
print(sendPacket(sock, hello()))
print(sendPacket(sock, hello()))
print(sendPacket(sock, hello()))
print(sendPacket(sock, hello()))
print(sendPacket(sock, hello()))
print(sendPacket(sock, hello()))
print(sendPacket(sock, hello()))
print(sendPacket(sock, hello()))
print(sendPacket(sock, hello()))
print(sendPacket(sock, hello()))
print(sendPacket(sock, hello()))
print(sendPacket(sock, hello()))
print(sendPacket(sock, hello()))
print(sendPacket(sock, hello()))
print(recvPacket(sock))
sock.close()
