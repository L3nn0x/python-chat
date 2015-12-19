import socket
import select
from common.utils import *
from common.protocol import *

SIZE = 4096

def emptySocket(sock):
    input = [sock]
    while True:
        inputReady, o, e = select.select(input, [], [], 0)
        if len(inputReady) == 0:
            break
        for s in inputReady:
            s.recv(SIZE)

def send(sock, data, encode = True):
    size = len(data)
    byte = list(str(size).encode("latin1"))
    if encode:
        byte += data.encode("latin1")
    else:
        byte += data
    byte = bytearray(byte)
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
    if size <= 1:
        emptySocket(sock)
        return None
    data = data[len(str(size)):]
    while len(data) < size and size - len(data) >= SIZE:
        data += sock.recv(SIZE).decode("latin1")
    if size > len(data):
        data += sock.recv(size - len(data)).decode("latin1")
    return data[:size + 1]


