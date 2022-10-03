import socket

id = 0
HOST = '127.0.0.1'
PORT = 1234
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))


while True:
    id += 1
    print("Aguardando requisição de número {s} ...".format(s=id))
    data, address = sock.recvfrom(1024)
    client_host, client_port = address
    msg = data.decode('utf-8')

    print("Requisição de id {s} recebida com sucesso!".format(s=id))
    resultado = 0
    msg_operação= msg.split()
    operador= msg_operação[1]
    num1 = float(msg_operação[0])
    num2 = float(msg_operação[2])

    if operador == '+':
        resultado = num1 + num2;
        print("{a} + {b} = {c}".format(a = num1, b=num2, c = resultado))
    elif operador == "-":
        resultado = num1 - num2;
        print("{a} - {b} = {c} ".format(a = num1, b=num2, c = resultado))
    elif operador == "*":
        resultado = num1 * num2;
        print("{a} * {b} = {c}".format(a = num1, b=num2, c = resultado))
    elif operador == "/":
        resultado = num1 + num2;
        print("{a} + {b} = {c}".format(a = num1, b=num2, c = resultado))

sock.close()



