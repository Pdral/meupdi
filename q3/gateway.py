import threading, socket, struct, json, objetos_pb2
import time

from temperatura import Temperatura

objetos = []
MCAST_GRP = "225.0.0.1"
MCAST_Port = 1334
LocalIP = '127.0.0.1'
temperatura = Temperatura()


def identifica(multi_sock):
    msg_dict = {'Code': 2}
    multi_sock.sendto(bytes(json.dumps(msg_dict), 'utf-8'), (MCAST_GRP, MCAST_Port))


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
        data, _ = sock.recvfrom(4096)
        data = json.loads(data.decode('utf-8'))
        tipo = data.pop('Tipo')
        if tipo == 2:
            temperatura.temp = data['Temp']
        elif tipo == 1:
            envia_planta(data, conn)
        elif tipo == 4:
            envia_luz(data, conn)


def recebe_app(conn, sock, multi_sock):
    request = objetos_pb2.Request()
    while True:
        data = conn.recv(4096)
        request.ParseFromString(data)
        if request.tipo == objetos_pb2.REGAR:
            zero = True
            for obj in objetos:
                if obj['Tipo'] == 1:
                    sock.sendto(bytes('2', 'utf-8'), (obj['IP'], obj['Porta']))
                    zero = False
            if zero:
                responde_app(True, "\nNão há plantas na estufa...\n", conn)
            else:
                responde_app(False, "\nPlantas regadas com sucesso!\n", conn)
        elif request.tipo == objetos_pb2.BUSCA:
            identifica(multi_sock)
            responde_app(False, "\nLista de objetos atualizada!\n", conn)
        else:
            if request.objeto == objetos_pb2.PLANTA:
                for objeto in objetos:
                    if objeto['Tipo'] == 1:
                        sock.sendto(bytes('1', 'utf-8'), (objeto['IP'], objeto['Porta']))
                time.sleep(3)
                responde_app(True, "Acabou", conn)
            elif request.objeto == objetos_pb2.SENSOR:
                zero = True
                for objeto in objetos:
                    if objeto['Tipo'] == 2:
                        envia_temp(conn)
                        zero = False
                        break
                if zero:
                    responde_app(True, "\nNão há sensores na estufa...\n", conn)
            elif request.objeto == objetos_pb2.AQUECEDOR:
                value = request.value
                zero = True
                for objeto in objetos:
                    if objeto['Tipo'] == 3:
                        sock.sendto(bytes(str(value), 'utf-8'), (objeto['IP'], objeto['Porta']))
                        responde_app(False, "\nTemperatura alterada com sucesso!\n", conn)
                        zero = False
                        break
                if zero:
                    responde_app(True, "\nNão há aquecedores na sala...\n", conn)
            elif request.objeto == objetos_pb2.LAMPADA:
                if request.modificar:
                    value = request.value
                    msg = {'Code': 2, 'Luz': str(value)}
                    zero = True
                    for objeto in objetos:
                        if objeto['Tipo'] == 4:
                            sock.sendto(bytes(json.dumps(msg), 'utf-8'), (objeto['IP'], objeto['Porta']))
                            responde_app(False, "\nLuminosidade alterada com sucesso!\n", conn)
                            zero = False
                            break
                    if zero:
                        responde_app(True, "\nNão há lâmpadas na estufa...\n", conn)
                else:
                    msg = {'Code': 1}
                    zero = True
                    for objeto in objetos:
                        if objeto['Tipo'] == 4:
                            sock.sendto(bytes(json.dumps(msg), 'utf-8'), (objeto['IP'], objeto['Porta']))
                            zero = False
                            break
                    if zero:
                        responde_app(True, "\nNão há lâmpadas na estufa...\n", conn)


def envia_planta(planta_dict, conn):
    response = objetos_pb2.Response()
    response.erro = False
    response.msg = "\nInformações da planta:\n"
    objects = objetos_pb2.Objetos()
    planta = objects.plantas.add()
    planta.agua = planta_dict['agua']
    planta.agua_min = planta_dict['agua_min']
    planta.luz_min = planta_dict['luz']
    planta.temp_min = planta_dict['temp_min']
    planta.temp_max = planta_dict['temp_max']
    planta.name = planta_dict['name']
    planta.vida = planta_dict['vida']
    response.objetos.CopyFrom(objects)
    pkg = response.SerializeToString()
    conn.sendall(pkg)


def envia_luz(luz, conn):
    response = objetos_pb2.Response()
    response.erro = False
    response.msg = "\nLuminosidade: "
    objects = objetos_pb2.Objetos()
    lamp = objetos_pb2.Lampada()
    lamp.luz = luz['Luz']
    objects.lampada.CopyFrom(lamp)
    response.objetos.CopyFrom(objects)
    pkg = response.SerializeToString()
    conn.sendall(pkg)


def envia_temp(conn):
    response = objetos_pb2.Response()
    response.erro = False
    response.msg = "\nTemperatura: "
    objects = objetos_pb2.Objetos()
    sensor = objetos_pb2.Sensor()
    sensor.temp = temperatura.temp
    objects.sensor.CopyFrom(sensor)
    response.objetos.CopyFrom(objects)
    pkg = response.SerializeToString()
    conn.sendall(pkg)


def responde_app(erro, msg, conn):
    response = objetos_pb2.Response()
    response.erro = erro
    response.msg = msg
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
#sock.settimeout(2)

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
