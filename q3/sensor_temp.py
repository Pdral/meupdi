import threading, socket, struct, json, atexit
import time

MCAST_GRP = "225.0.0.1"
MCAST_Port = 1234
LocalIP = '127.0.0.1'
temp = '28'


def identifica(multi_sock):
    msg_dict = {"Code": 1, "Tipo": 2, "IP": LocalIP, "Porta": 1238}
    multi_sock.sendto(bytes(json.dumps(msg_dict), 'utf-8'), (MCAST_GRP, MCAST_Port))


def recebe_multi(multi_sock):
    while True:
        data = json.loads(multi_sock.recv(4096).decode('utf-8'))
        if data['Code'] == 2:
            identifica(multi_sock)


def informa_gateway(sock):
    _, end = sock.recvfrom(4096)
    while True:
        msg = {'Tipo': 2, 'Temp': int(temp)}
        sock.sendto(bytes(json.dumps(msg)), end)
        time.sleep(10)


def recebe_temp(sock_temp):
    print("Sensor iniciado com sucesso!")
    while True:
        temp = sock_temp.recv(4096).decode('utf-8')


def excluir(multi_sock):
    msg_dict = {"Code": 3}
    multi_sock.sendto(bytes(json.dumps(msg_dict), 'utf-8'), (MCAST_GRP, MCAST_Port))
    multi_sock.close()


multi_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
multi_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
multi_sock.bind(('', MCAST_Port))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
multi_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
identifica(multi_sock)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LocalIP, 1238))

sock_temp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_temp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_temp.bind(('', 1235))
sock_temp.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

atexit.register(excluir, multi_sock)

t1 = threading.Thread(target=recebe_multi, daemon=True, args=(multi_sock,))
t1.start()
t2 = threading.Thread(target=informa_gateway, daemon=True, args=(sock,))
t2.start()
t3 = threading.Thread(target=recebe_temp, args=(sock_temp,))
t3.start()
