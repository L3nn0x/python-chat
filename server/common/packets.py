import socket
import select
from common.utils import *
from common.protocol import *

def send(packet, isEncoded = False):
    if not packet:
        return None
    data = packet[0].encode("utf-8")
    for arg in packet[1:]:
        if not isEncoded:
            data = data + " ".encode("utf-8") + arg.encode("utf-8")
        else:
            data = data + " ".encode("utf-8") + bytes(arg)
    data = bytes(str(len(data)).encode("utf-8")) + data
    return data

def recv(sock):
    data = sock.recv(SIZE)
    print(data)
    print(data[0])
