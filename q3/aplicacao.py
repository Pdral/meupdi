import socket, objetos_pb2, time


SERVIDOR_IP = '127.0.0.1'
SERVIDOR_PORTA = 1233
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVIDOR_IP, SERVIDOR_PORTA))
request = objetos_pb2.Request()
response = objetos_pb2.Response()
print("Bem vindo ao gerenciamento de estufa!\n")
while True:
    print("Insira a opção desejada:")
    print("1 - Checkup das plantas")
    print("2 - Verificar temperatura do sensor")
    print("3 - Alterar temperatura do aquecedor")
    print("4 - Verificar luminosidade da lâmpada")
    print("5 - Alterar luminosidade da lâmpada")
    print("6 - Regar plantas")
    print("7 - Buscar novos aparelhos")
    opc = int(input())
    if opc == 1:
        request.tipo = objetos_pb2.OBJETO
        request.objeto = objetos_pb2.PLANTA
        sock.sendall(request.SerializeToString())
        zero = True
        while True:
            response.ParseFromString(sock.recv(4096))
            if response.erro:
                if zero:
                    print("\nNão há plantas na estufa...\n")
                break
            else:
                for planta in response.objetos.plantas:
                    print("\nNome: {a}\nNível de água: {b}/5\nNível de água mínimo: {c}/5\n"
                          "Luminosidade mínima: {d}/5\nIntervalo de temperatura necessário: [{e} - {f}]\n"
                          "Vida: {g}/10\n".format(a=planta.name, b=planta.agua, c=planta.agua_min,
                                                d=planta.luz_min, e=planta.temp_min, f=planta.temp_max,
                                                g=planta.vida))
                zero = False
    elif opc == 2:
        request.objeto = objetos_pb2.SENSOR
        request.tipo = objetos_pb2.OBJETO
        sock.sendall(request.SerializeToString())
        response.ParseFromString(sock.recv(4096))
        time.sleep(3)
        if response.erro:
            print(response.msg)
        else:
            print(response.msg + str(response.objetos.sensor.temp) + '\n')
    elif opc == 3:
        print("Informe o valor desejado para a temperatura (10-40):")
        try:
            v = int(input())
            if v not in range(10, 41):
                print("Valor inválido!")
            else:
                request.objeto = objetos_pb2.AQUECEDOR
                request.tipo = objetos_pb2.OBJETO
                request.value = v
                sock.sendall(request.SerializeToString())
                response.ParseFromString(sock.recv(4096))
                time.sleep(3)
                print(response.msg)
        except:
            print("O valor informado não foi um inteiro!")
    elif opc == 4:
        request.objeto = objetos_pb2.LAMPADA
        request.tipo = objetos_pb2.OBJETO
        request.modificar = False
        sock.sendall(request.SerializeToString())
        response.ParseFromString(sock.recv(4096))
        time.sleep(3)
        if response.erro:
            print(response.msg)
        else:
            print(response.msg + str(response.objetos.lampada.luz) + '\n')
    elif opc == 5:
        print("Informe o valor desejado para a luminosidade (1-5):")
        try:
            v = int(input())
            if v not in range(1, 6):
                print("Valor inválido!")
            else:
                request.objeto = objetos_pb2.LAMPADA
                request.tipo = objetos_pb2.OBJETO
                request.value = v
                request.modificar = True
                sock.sendall(request.SerializeToString())
                response.ParseFromString(sock.recv(4096))
                time.sleep(3)
                print(response.msg)
        except:
            print("O valor informado não foi um inteiro!")

    elif opc == 6:
        request.tipo = objetos_pb2.REGAR
        sock.sendall(request.SerializeToString())
        response.ParseFromString(sock.recv(4096))
        time.sleep(3)
        print(response.msg)
    elif opc == 7:
        request.tipo = objetos_pb2.BUSCA
        sock.sendall(request.SerializeToString())
        response.ParseFromString(sock.recv(4096))
        time.sleep(3)
        print(response.msg)
