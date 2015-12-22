import pickle

SIZE = 4096
SIZESIZE = 2

class   Packet:
    def __init__(self, packetType, *args, **kwargs):
        self.packetType = packetType
        self.args = list(args)
        self.kwargs = kwargs

    def append(self, *args, **kwargs):
        self.args.extend(args)
        self.kwargs.update(kwargs)

    def serialize(self):
        return pickle.dumps(self)
    
    def __str__(self):
        return "Packet type: {}\nArgs: {}\nKwargs: {}".format(self.packetType, self.args, self.kwargs)

    @staticmethod
    def deserialize(data):
        return pickle.loads(data)

def sendPacket(sock, packet):
    data = packet.serialize()
    size = len(data)
    if size >= pow(256, SIZESIZE):
        return False
    packets = []
    while len(data) > SIZE:
        packets.append(data[:SIZE])
        data = data[SIZE:]
    packets.append(data)
    sock.sendall(size.to_bytes(SIZESIZE, byteorder="big"))
    for packet in packets:
        sock.sendall(packet)
    return True

def recvPacket(sock):
    size = int.from_bytes(sock.recv(SIZESIZE), byteorder="big")
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
