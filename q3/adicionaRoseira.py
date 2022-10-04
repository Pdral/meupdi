from roseira import Roseira
import threading, socket, struct, json, time, objetos_pb2

roseira = Roseira()
MCAST_GRP = "225.0.0.1"
MCAST_Port = 1234
LocalIP = '127.0.0.1'

def identifica(multi_sock):
    msg_dict = {"Code": 1, "Tipo": 1, "IP": LocalIP, "Porta": 1235}
    multi_sock.sendto(bytes(json.dumps(msg_dict), 'utf-8'), (MCAST_GRP, MCAST_Port))

def recebe_multi(multi_sock):
    while True:
        data = json.loads(multi_sock.recv(4096).decode('utf-8'))
        if data['Code'] == 2:
            identifica(multi_sock)

def recebe_gateway(sock):
    while True:
        _, end = sock.recvfrom(4096)
        roseira_serialize = objetos_pb2.Planta()
        roseira_serialize.agua = roseira.agua
        roseira_serialize.agua_min = roseira.agua_min
        roseira_serialize.luz_min = roseira.luz_min
        roseira_serialize.temp_min = roseira.temp_min
        roseira_serialize.temp_max = roseira.temp_max
        pkg = roseira_serialize.SerializeToString()
        sock.sendto(pkg, end)

def esta_viva(sock_temp, sock_luz, multi_sock):
    while roseira.viva:
        time.sleep(10)
        data_temp = sock_temp.recv(4096).decode('utf-8')
        data_luz = sock_luz.recv(4096).decode('utf-8')
        roseira.verifica_ambiente(int(data_luz), int(data_temp))
    msg_dict = {"Code": 3}
    multi_sock.sendto(bytes(json.dumps(msg_dict), 'utf-8'), (MCAST_GRP, MCAST_Port))
    multi_sock.close()

def consome_agua():
    roseira.consome_agua()


multi_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
multi_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
multi_sock.bind(('', MCAST_Port))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
multi_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
identifica(multi_sock)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LocalIP, 1235))

sock_temp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((MCAST_GRP, 1235))

sock_luz = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((MCAST_GRP, 1236))

t1 = threading.Thread(target=recebe_multi, daemon=True, args=(multi_sock,))
t1.start()
t2 = threading.Thread(target=recebe_gateway, daemon=True, args=(sock,))
t2.start()
t3 = threading.Thread(target=consome_agua, daemon=True)
t3.start()
t4 = threading.Thread(target=esta_viva, args=(sock_temp, sock_luz,))
t4.start()
