import pickle
from common.utils import atoi

SIZE = 4096
MAXPACKETSIZE = 65536
SIZESIZE = 5

class   Packet:
    def __init__(self, packetType, *args, **kwargs):
        self.packetType = packetType
        self.args = args
        self.kwargs = kwargs

    def append(self, *args, **kwargs):
        self.args.extend(args)
        self.kwargs.update(kwargs)

    def serialize(self):
        return pickle.dumps(self)

    @staticmethod
    def deserialize(data):
        return pickle.loads(data)

def sendPacket(sock, packet):
    data = packet.serialize()
    size = len(data)
    if size >= MAXPACKETSIZE:
        return
    packets = []
    while len(data) > SIZE:
        packets.append(data[:SIZE])
        data = data[SIZE:]
    packets.append(data)
    sock.sendall(str(size).encode("utf-8"))
    for packet in packets:
        sock.sendall(packet)

def recvPacket(sock):
    size = atoi(sock.recv(SIZESIZE).decode("utf-8"))
    if size < 1:
        return None
    if size < SIZE:
        return Packet.deserialize(sock.recv(size))
    data = bytes()
    while len(data) < size and size - len(data) >= SIZE:
        data = data + sock.recv(SIZE)
    if size > len(data):
        data = data + sock.recv(size - len(data))
    return Packet.deserialize(data)
