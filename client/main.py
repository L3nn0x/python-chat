import socket
import select
from common.protocol import *
from common.packet import *

def connection(sock, login, password):
    packets = [hello(), credentials(login, password)]
    sent = False
    while True:
        rlist, wlist, xlist = select.select([sock], [sock], [])
        if len(wlist) and len(packets) and not sent:
            res = sendPacket(sock, packets[0])
            if not res:
                return False, "Error while sending a packet"
            sent = True
        if len(rlist):
            packet = recvPacket(sock)
            if not packet:
                return False, "Error while receiving a packet"
            if packets[0].packetType == HELLO and packet.packetType != HELLO:
                return False, "Error of protocol"
            elif packets[0].packetType == HELLO and packet.packetType == HELLO:
                sent = False
                packets = packets[1:]
            elif packets[0].packetType == CREDENTIALS:
                if packet.packetType == NOK:
                    return False, packet.get("reason")
                else:
                    return True, ""

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 1234))
login = input("Login > ")

ok, res = connection(sock, login, 'test')
if not ok:
    print("Connection error:", res)
    exit(0)

packets = []

while True:
    try:
        rlist, wlist, xlist = select.select([0, sock], [sock], [])
        if 0 in rlist:
            data = input()
            packets.append(msg(login, 'eneral', data.rstrip('\n')))
        if sock in rlist:
            packet = recvPacket(sock)
            if not packet:
                print("Connection reset by peer")
                break
            if packet.packetType == MSG:
                print("{} on {}(id:{}) sent: {}".format(packet.get('source'), packet.get('destination'), packet.get('id'), packet.get('data')))
            else:
                print(packet)
        if len(wlist) and len(packets):
            res = sendPacket(sock, packets[0])
            if res:
                packets = packets[1:]
            else:
                print("Error while sending:", packets[0])
    except Exception as e:
        print("Exception:", e)
        break
sock.close()
