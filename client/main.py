import socket
import select
from common.packets import send, receive
from common.protocol import *

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 1234))

send(sock, HELLO)
data = receive(sock)
if not data or data.split(' ')[0] != HELLO:
    print("Impossible to connect to the server:", data)
    sock.close()
    exit(0)
login = input("login: ")
send(sock, protFormat(CREDENTIALS, login, "bla"))
data = receive(sock)
if not data or data.split(' ')[0] != OK:
    print("Impossible to login")
    sock.close()
    exit(0)
channels = []
data = None
print("Downloading channels")
while data != OK:
    data = receive(sock)
    if data.split(' ')[0] == CHAN:
        channels.append(data.split(' ')[1])
data = None
print("Channels:", *channels)
channel = channels[0]
print("Current channel:", channel)
while data != END:
    try:
        data = None
        print("> ", end='', flush=True)
        rlist, wlist, xlist = select.select([0, sock], [], [])
        if 0 in rlist:
            data = input()
            data = data.rstrip('\n')
            if not len(data):
                continue
            send(sock, protFormat(SEND_MSG, channel, data))
            data = receive(sock)
            if data == NOK:
                print("The last message couldn't be delivered")
        elif sock in rlist:
            data = receive(sock)
            if not data:
                data = END
            data = data.split(' ')
            if data[0] == MSG:
                print(data[1], "sent in channel", data[2], ":", ' '.join(data[3:]))
            elif data[0] == END:
                print("The server closed the connection")
            else:
                print(data)
    except:
        break
sock.close()
