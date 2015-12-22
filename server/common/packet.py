import pickle

SIZE_NETWORK_PACKET = 4096  # max network frame size sent at once
SIZE_LENGTH = 2             # max total size for one Packet: 256^SIZE_LENGTH

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
        try:
            return pickle.loads(data)
        except:
            return None

# Return True if the Packet was sent, False otherwise
def sendPacket(sock, packet):
    data = packet.serialize()
    size = len(data)
    if size >= pow(256, SIZE_LENGTH):
        return False
    packets = []
    while len(data) > SIZE_NETWORK_PACKET:
        packets.append(data[:SIZE_NETWORK_PACKET])
        data = data[SIZE_NETWORK_PACKET:]
    packets.append(data)
    sock.sendall(size.to_bytes(SIZE_LENGTH, byteorder="big"))
    for packet in packets:
        sock.sendall(packet)
    return True

# Return None if no packet was able to be received, otherwise returns the correctly formated Packet
def recvPacket(sock):
    size = int.from_bytes(sock.recv(SIZE_LENGTH), byteorder="big")
    if size < 1:
        return None
    if size < SIZE_NETWORK_PACKET:
        return Packet.deserialize(sock.recv(size))
    data = bytes()
    while len(data) < size and size - len(data) >= SIZE_NETWORK_PACKET:
        data = data + sock.recv(SIZE_NETWORK_PACKET)
    if size > len(data):
        data = data + sock.recv(size - len(data))
    return Packet.deserialize(data)
