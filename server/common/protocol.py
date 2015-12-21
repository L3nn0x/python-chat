SIZE = 4096

# protocol

def createPacket(protocol, *args):
    try:
        data = [protocol]
        for arg in args[:__protocol_args[protocol]]:
            data.append(arg)
        return data
    except:
        return None

def openPacket(packet):
    packet = packet.split(' ')
    try:
        protocol = packet[0]
        data = []
        packet = packet[1:]
        for arg in range(__protocol_args[protocol]):
            data.append(packet[arg])
        return protocol, data
    except:
        return None

# from both:
HELLO = "HELLO"         # first thing sent by the client and the server
RECV = "RECV"           # indicates that the packet has been received

# from client:
CREDENTIALS = "CREDENTIALS" # CREDENTIALS login password
GET_PROFILE = "GPRO"    # get the profile of a specific client (by id) if no id is provided return the current profile.
SEND_MSG = "SMSG"       # send a message SMSG dest msg

# from server:
END = "END"             # server is closing the connection
OK = "OK"               # response from the server
NOK = "NOK"             # response from the server
MSG = "MSG"             # send a message (MSG src dest msg)
CHAN = "CHAN"           # channel name CHAN name (unique names)
PROFILE = "PRO"         # server answer with the profile details

__protocol_args = {
        HELLO: 0,
        RECV: 0,
        CREDENTIALS: 2,
        GET_PROFILE: 1,
        SEND_MSG: 2,
        END: 0,
        OK: 0,
        NOK: 0,
        MSG: 3,
        CHAN: 1,
        PROFILE: 1,
}
