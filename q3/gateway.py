import threading, socket, struct, json, time, objetos_pb2

objetos = []
MCAST_GRP = "225.0.0.1"
MCAST_Port = 1234
LocalIP = '127.0.0.1'
temp = 28


def identifica(multi_sock):
    msg_dict = {"Code": 2}
    multi_sock.sendto(bytes(json.dumps(msg_dict), 'utf-8'), (MCAST_GRP, MCAST_Port))
    objetos = []


def recebe_multi(multi_sock, sock):
    while True:
        data = json.loads(multi_sock.recv(4096).decode('utf-8'))
        code = data.pop('Code')
        if code == 1:
            if data not in objetos:
                objetos.append(data)
            if data['Tipo'] == 2:
                sock.sendto(bytes('1', 'utf-8'), (data['IP'], data['Porta']))
        if code == 3:
                objetos.remove(data)


def recebe_sock(sock, conn):
    while True:
        data = json.loads(sock.recv(4096).decode('utf-8'))
        tipo = data.pop('Tipo')
        if tipo == 2:
            temp = data['Temp']
        elif tipo == 1:
            responde_app(False, "informações da planta", [data])
        elif tipo == 3:
            responde_app(False, "Luminosidade", [data])

def recebe_app(conn, sock, multi_sock):
    while True:
        request = objetos_pb2.Request()
        request.ParseFromString(conn.recv(4096))
        if request.tipo == objetos_pb2.REGAR:
            for obj in objetos:
                if obj['Tipo'] == 1:
                    sock.sendto(bytes('2', 'utf-8'), (obj['IP'], obj['Porta']))
            responde_app(False, "Plantas regadas com sucesso!", [])
        elif request.tipo == objetos_pb2.BUSCA:
            identifica(multi_sock)
            time.sleep(5)
            response = objetos_pb2.Objetos()

            conn.sendall(response.SerializeToString())
        else:
            objeto = objetos[request.id]
            if objeto['Tipo'] == 1:
                sock.sendto(bytes('1', 'utf-8'), (objeto['IP'], objeto['Porta']))
            elif objeto['Tipo'] == 2:
                responde_app(False, "Temperatura", [objeto])
            elif objeto['Tipo'] == 3:
                value = request.value
                sock.sendto(bytes(str(value), 'utf-8'), (objeto['IP'], objeto['Porta']))
                responde_app(False, "Temperatura alterada com sucesso!", [])
            elif objeto['Tipo'] == 4:
                if request.modificar:
                    value = request.value
                    msg = {'Code': 2, 'Luz': str(value)}
                    sock.sendto(bytes(json.dumps(msg), 'utf-8'), (objeto['IP'], objeto['Porta']))
                    responde_app(False, "Luminosidade alterada com sucesso!", [])
                else:
                    msg = {'Code': 1}
                    sock.sendto(bytes(json.dumps(msg), 'utf-8'), (objeto['IP'], objeto['Porta']))


def responde_app(erro, msg, objs):
    response = objetos_pb2.Response()
    response.erro = erro
    response.msg = msg
    objects = objetos_pb2.Objetos()
    for obj in objs:
        if obj['Tipo'] == 1:
            planta = objetos_pb2.Planta()
            planta.agua = obj['agua']
            planta.agua_min = obj['agua_min']
            planta.luz_min = obj['luz']
            planta.temp_min = obj['temp_min']
            planta.temp_max = obj['temp_max']
            planta.name = obj['name']
            objects.plantas.add(planta)
        elif obj['Tipo'] == 2:
            sensor = objetos_pb2.Sensor()
            sensor.temp = temp
            objects.sensor = sensor
        elif obj['Tipo'] == 4:
            lamp = objetos_pb2.Lampada()
            lamp.luz = obj['Luz']
            objects.lampada = lamp
    response.objetos = objects
    pkg = response.SerializeToString()
    conn.sendall(pkg)


multi_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
multi_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
multi_sock.bind(('', MCAST_Port))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
multi_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
identifica(multi_sock)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((LocalIP, 1234))

sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_tcp.bind((LocalIP, 1233))
sock_tcp.listen()
print("Gateway iniciado com sucesso!")
conn, addr = sock_tcp.accept()

t1 = threading.Thread(target=recebe_multi, daemon=True, args=(multi_sock, sock,))
t1.start()
t2 = threading.Thread(target=recebe_sock, daemon=True, args=(sock, conn,))
t2.start()
t3 = threading.Thread(target=recebe_app, args=(conn, sock, multi_sock))
t3.start()
