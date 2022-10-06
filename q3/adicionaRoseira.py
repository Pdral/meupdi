from roseira import Roseira
import threading, socket, struct, json, time
from temperatura import Temperatura
from luminosidade import Luminosidade

roseira = Roseira()
MCAST_GRP = "225.0.0.1"
MCAST_Port = 1334
LocalIP = '127.0.0.1'
temperatura = Temperatura()
luminosidade = Luminosidade()


def identifica(multi_sock):
    msg_dict = {"Code": 1, "Tipo": 1, "IP": LocalIP, "Porta": 1235}
    multi_sock.sendto(bytes(json.dumps(msg_dict), 'utf-8'), (MCAST_GRP, MCAST_Port))


def recebe_multi(multi_sock):
    while roseira.viva:
        try:
            data = json.loads(multi_sock.recv(4096).decode('utf-8'))
            if data['Code'] == 2:
                identifica(multi_sock)
        except:
            pass


def recebe_gateway(sock):
    while roseira.viva:
        try:
            data, end = sock.recvfrom(4096)
            code = data.decode('utf-8')
            if code == '1':
                msg = roseira.cria_dict()
                msg['Tipo'] = 1
                sock.sendto(bytes(json.dumps(msg), 'utf-8'), end)
            else:
                roseira.agua = 5
        except:
            pass


def esta_viva(multi_sock, sock, sock_temp, sock_luz):
    print("Roseira iniciada com sucesso!")
    while roseira.viva:
        time.sleep(15)
        roseira.verifica_ambiente(luminosidade.luz, temperatura.temp)
    msg_dict = {"Code": 3, "Tipo": 1, "IP": LocalIP, "Porta": 1235}
    time.sleep(2)
    multi_sock.sendto(bytes(json.dumps(msg_dict), 'utf-8'), (MCAST_GRP, MCAST_Port))
    multi_sock.close()
    sock.close()
    sock_temp.close()
    sock_luz.close()


def consome_agua():
    roseira.consome_agua()


def recebe_temp(sock_temp):
    while roseira.viva:
        try:
            temperatura.temp = int(sock_temp.recv(4096).decode('utf-8'))
        except:
            pass


def recebe_luz(sock_luz):
    while roseira.viva:
        try:
            luminosidade.luz = int(sock_luz.recv(4096).decode('utf-8'))
        except:
            pass


multi_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
multi_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
multi_sock.bind(('', MCAST_Port))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
multi_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
multi_sock.settimeout(2)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LocalIP, 1235))
sock.settimeout(2)

sock_temp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_temp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_temp.bind(('', 1335))
sock_temp.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
sock_temp.settimeout(2)

sock_luz = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_luz.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_luz.bind(('', 1336))
sock_luz.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
sock_luz.settimeout(2)

t1 = threading.Thread(target=recebe_multi, daemon=True, args=(multi_sock,))
t1.start()
t2 = threading.Thread(target=recebe_gateway, daemon=True, args=(sock,))
t2.start()
t3 = threading.Thread(target=consome_agua, daemon=True)
t3.start()
t5 = threading.Thread(target=recebe_temp, daemon=True, args=(sock_temp,))
t5.start()
t6 = threading.Thread(target=recebe_luz, daemon=True, args=(sock_luz,))
t6.start()
t4 = threading.Thread(target=esta_viva, args=(multi_sock, sock, sock_temp, sock_luz,))
t4.start()

identifica(multi_sock)