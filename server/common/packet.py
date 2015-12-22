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
    try:
        sent = sock.send(size.to_bytes(SIZE_LENGTH, byteorder="big"))
        if sent != SIZE_LENGTH:
            return False
        for packet in packets:
            if sock.send(packet) != len(packet):
                return False
        return True
    except (ConnectionResetError, BrokenPipeError):
        return False

# Returns None if no packet was able to be received, otherwise returns the correctly formated Packet
def recvPacket(sock):
    try:
        size = int.from_bytes(sock.recv(SIZE_LENGTH), byteorder="big")
        if size < 1:
            return None
        data = bytes()
        while len(data) < size and size - len(data) >= SIZE_NETWORK_PACKET:
            packet = sock.recv(SIZE_NETWORK_PACKET)
            if packet == '':
                return None
            data = data + packet
        if size > len(data):
            packet = sock.recv(size - len(data))
            return None
            if packet == '':
                return None
            data = data + packet
        return Packet.deserialize(data)
    except (ConnectionResetError, BrokenPipeError):
        return None
