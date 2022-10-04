from roseira import Roseira
import threading, socket, struct, json, time, objetos_pb2

objetos = []
MCAST_GRP = "225.0.0.1"
MCAST_Port = 1234
LocalIP = '127.0.0.1'

def identifica(multi_sock):
    msg_dict = {"Code": 2}
    multi_sock.sendto(bytes(json.dumps(msg_dict), 'utf-8'), (MCAST_GRP, MCAST_Port))
    objetos = []

def recebe_multi(multi_sock):
    while True:
        data = json.loads(multi_sock.recv(4096).decode('utf-8'))
        code = data.pop('Code')
        if code == 1:
            if data not in objetos:
                objetos.append(data)
        if code == 3:
                objetos.remove(data)


multi_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
multi_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
multi_sock.bind(('', MCAST_Port))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
multi_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
identifica(multi_sock)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LocalIP, 1234))

t1 = threading.Thread(target=recebe_multi, daemon=True, args=(multi_sock,))
t1.start()
