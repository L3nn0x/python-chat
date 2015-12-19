SIZE = 4096

# protocol

def protFormat(protocol, *args):
    dic = {
            HELLO: lambda l: HELLO,
            CREDENTIALS: lambda l: CREDENTIALS + " " + l[0] + " " + l[1],
            GET_PROFILE: lambda l: GET_PROFILE + " " + l[0],
            SEND_MSG: lambda l: SEND_MSG + " " + l[0] + " " + l[1],
            END: lambda l: END,
            OK: lambda l: OK,
            NOK: lambda l: NOK,
            MSG: lambda l: MSG + " " + l[0] + " " + l[1] + " " + l[2],
            CHAN: lambda l: CHAN + " " + l[0],
            PROFILE: lambda l: PROFILE + " " + l[0],
    }
    return dic[protocol](args)

# from both:
HELLO = "HELLO"         # first thing sent by the client and the server
RECV = "RECV"           # indicates that the packet has been received

# from client:
CREDENTIALS = "CREDENTIALS" # CREDENTIALS login password
GET_PROFILE = "GPRO"    # get the profile of a specific client (by id) if no id is provided return the current profile.
SEND_MSG = "SMSG"       # send a message SMSG dest msg

# from server:
END = "END"             # server is closing the connection
NOK = "NOK"             # response from the server
MSG = "MSG"             # send a message (MSG src dest msg)
CHAN = "CHAN"           # channel name CHAN name (unique names)
PROFILE = "PRO"         # server answer with the profile details
