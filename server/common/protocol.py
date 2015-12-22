from common.packet import Packet

def hello():
    return Packet(HELLO)

def ok():
    return Packet(OK)

def nok():
    return Packet(NOK)

def credentials(login, password):
    return Packet(CREDENTIALS, login=login, password=password)

def channels(*channels):
    return Packet(CHAN, *channels)

def msg(source, dest, msg):
    return Packet(MSG, source=source, destination=dest, data=msg)

# protocol
HELLO = "HELLO"                 # first packet sent
CREDENTIALS = "CREDENTIALS"     # with login=<> and password=<> (encrypted)
OK = "OK"                       # ok packet
NOK = "NOK"                     # not ok packet
CHAN = "CHAN"                   # send channel names (all of them) and people inside
MSG = "MSG"                     # send a msg with source, dest and data

# normal communication (if packet isn't good, deconnection)
"""Client connects: 
    - HELLO
                        - HELLO
    - CREDENTIALS
                        - OK|NOK
                        - CHAN
    - OK|NOK
                        - (if NOK resend, else wait)
    - MSG
                        - OK|NOK
    - (if NOK resend, else continue)
"""
