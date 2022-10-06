import threading, socket, struct, json
import time

from luminosidade import Luminosidade

MCAST_GRP = "225.0.0.1"
MCAST_Port = 1334
LocalIP = '127.0.0.1'
luminosidade = Luminosidade()


def identifica(multi_sock):
    msg_dict = {"Code": 1, "Tipo": 4, "IP": LocalIP, "Porta": 1240}
    multi_sock.sendto(bytes(json.dumps(msg_dict), 'utf-8'), (MCAST_GRP, MCAST_Port))


def recebe_multi(multi_sock):
    while luminosidade.run:
        try:
            data = json.loads(multi_sock.recv(4096).decode('utf-8'))
            if data['Code'] == 2:
                identifica(multi_sock)
        except:
            pass


def recebe_gateway(sock, sock_luz):
    while luminosidade.run:
        try:
            data, end = sock.recvfrom(4096)
            msg = json.loads(data.decode('utf-8'))
            if msg['Code'] == 1:
                pkg = {'Tipo': 4, 'Luz': int(luminosidade.luz)}
                sock.sendto(bytes(json.dumps(pkg), 'utf-8'), end)
            elif msg['Code'] == 2:
                luminosidade.luz = msg['Luz']
                sock_luz.sendto(bytes(luminosidade.luz, 'utf-8'), (MCAST_GRP, 1336))
        except:
            pass


def main(multi_sock, sock, sock_luz):
    print("Lâmpada iniciada com sucesso!")
    print("Digite '\\quit' para sair")
    x = ''
    while x != '/quit':
        x = input()
    luminosidade.run = False
    msg_dict = {"Code": 3, "Tipo": 4, "IP": LocalIP, "Porta": 1240}
    time.sleep(2)
    multi_sock.sendto(bytes(json.dumps(msg_dict), 'utf-8'), (MCAST_GRP, MCAST_Port))
    multi_sock.close()
    sock.close()
    sock_luz.close()


multi_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
multi_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
multi_sock.bind(('', MCAST_Port))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
multi_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
multi_sock.settimeout(2)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LocalIP, 1240))
sock.settimeout(2)

sock_luz = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_luz.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_luz.bind(('', 1336))
sock_luz.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
sock_luz.settimeout(2)

t1 = threading.Thread(target=recebe_multi, daemon=True, args=(multi_sock,))
t1.start()
t2 = threading.Thread(target=recebe_gateway, daemon=True, args=(sock,sock_luz,))
t2.start()
t3 = threading.Thread(target=main, args=(multi_sock, sock, sock_luz,))
t3.start()

identifica(multi_sock)
