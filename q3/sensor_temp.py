import threading, socket, struct, json
import time
from temperatura import Temperatura

MCAST_GRP = "225.0.0.1"
MCAST_Port = 1334
LocalIP = '127.0.0.1'
temperatura = Temperatura()


def identifica(multi_sock):
    msg_dict = {"Code": 1, "Tipo": 2, "IP": LocalIP, "Porta": 1238}
    multi_sock.sendto(bytes(json.dumps(msg_dict), 'utf-8'), (MCAST_GRP, MCAST_Port))


def recebe_multi(multi_sock):
    while temperatura.run:
        try:
            data = json.loads(multi_sock.recv(4096).decode('utf-8'))
            if data['Code'] == 2:
                identifica(multi_sock)
        except:
            pass


def informa_gateway(sock):
    _, end = sock.recvfrom(4096)
    while temperatura.run:
        msg = {'Tipo': 2, 'Temp': temperatura.temp}
        sock.sendto(bytes(json.dumps(msg), 'utf-8'), end)
        time.sleep(10)


def recebe_temp(sock_temp):
    while temperatura.run:
        try:
            temperatura.temp = int(sock_temp.recv(4096).decode('utf-8'))
            print(temperatura.temp)
        except:
            pass


def main(multi_sock, sock, sock_temp):
    print("Sensor iniciado com sucesso!")
    print("Digite '\\quit' para sair")
    x = ''
    while x != '/quit':
        x = input()
    temperatura.run = False
    msg_dict = {"Code": 3, "Tipo": 2, "IP": LocalIP, "Porta": 1238}
    time.sleep(2)
    multi_sock.sendto(bytes(json.dumps(msg_dict), 'utf-8'), (MCAST_GRP, MCAST_Port))
    multi_sock.close()
    sock.close()
    sock_temp.close()


multi_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
multi_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
multi_sock.bind(('', MCAST_Port))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
multi_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
multi_sock.settimeout(2)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LocalIP, 1238))

sock_temp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_temp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_temp.bind(('', 1335))
sock_temp.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
sock_temp.settimeout(2)

t1 = threading.Thread(target=recebe_multi, daemon=True, args=(multi_sock,))
t1.start()
t2 = threading.Thread(target=informa_gateway, daemon=True, args=(sock,))
t2.start()
t3 = threading.Thread(target=recebe_temp, daemon=True, args=(sock_temp,))
t3.start()
t4 = threading.Thread(target=main, args=(multi_sock, sock, sock_temp))
t4.start()

identifica(multi_sock)
