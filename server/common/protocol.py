from common.packet import Packet

def hello():
    return Packet(HELLO)

def ok():
    return Packet(OK)

def nok(reason=""):
    return Packet(NOK, reason=reason)

def credentials(login, password):
    return Packet(CREDENTIALS, login=login, password=password)

# TODO: send the history of each channel along
def channels(**channels):
    return Packet(CHAN, **channels)

def msg(source, dest, msg):
    return Packet(MSG, source=source, destination=dest, data=msg)

# protocol
HELLO = "HELLO"                 # first packet sent
CREDENTIALS = "CREDENTIALS"     # with login=<> and password=<> (encrypted)
OK = "OK"                       # ok packet
NOK = "NOK"                     # not ok packet
CHAN = "CHAN"                   # send channel names (public ones), people inside and the history
PROFILE = "PROFILE"             # send all accounts profiles or an updated one
MSG = "MSG"                     # send a msg with source, dest and data
EDIT = "EDIT"                   # edit/delete an already sent message (msg id, channel, new message)

# normal communication (if packet isn't good, deconnection)
"""Client connects: 
    - HELLO
                        - HELLO
    - CREDENTIALS
                        - OK|NOK(reason)
                        - PROFILES
                        - CHAN
    - MSG
                        - OK|NOK(reason)
    - (if NOK resend/reconnect, else continue)
                        - PROFILE (updated profile)
                        - MSG
    - PROFILE
                        - OK|NOK(reason)
"""
