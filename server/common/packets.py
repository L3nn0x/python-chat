import socket
import select
from common.utils import *

SIZE = 4

def emptySocket(sock):
    input = [sock]
    while True:
        inputReady, o, e = select.select(input, [], [], 0)
        if len(inputReady) == 0:
            break
        for s in inputReady:
            s.recv(SIZE)

def send(sock, data):
    size = len(data)
    size += len(str(size))
    byte = str(size)
    byte += str(data)
    byte = bytearray(byte, "latin1")
    packets = []
    while len(byte) >= SIZE:
        packets.append(byte[:SIZE])
        byte = byte[SIZE:]
    packets.append(byte)
    for packet in packets:
        sock.sendall(packet)

def receive(sock):
    data = sock.recv(SIZE).decode("latin1")
    size = atoi(data)
    if size == 0:
        emptySocket(sock)
        return ""
    while len(data) < size and size - len(data) >= SIZE:
        data += sock.recv(SIZE).decode("latin1")
    data += sock.recv(size - len(data)).decode("latin1")
    return data[len(str(size)):]


