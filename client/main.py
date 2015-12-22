import socket
import select
from common.protocol import *
from common.packet import *

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 1234))
login = input("Login > ")
packets = [hello(), credentials(login, 'test'), ok()]

while True:
    try:
        rlist, wlist, xlist = select.select([0, sock], [sock], [])
        if 0 in rlist:
            data = input()
            packets.append(msg(login, 'general', data.rstrip('\n')))
        if sock in rlist:
            packet = recvPacket(sock)
            if not packet:
                break
            if packet.packetType == MSG:
                print("{} on {} sent: {}".format(packet.get('source'), packet.get('destination'), packet.get('data')))
            else:
                print(packet)
        elif len(wlist) and len(packets):
            res = sendPacket(sock, packets[0])
            if res:
                packets = packets[1:]
    except Exception as e:
        print("Exception:", e)
        break
sock.close()
