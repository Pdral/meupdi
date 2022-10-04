import socket

print("Bem vindo à calculadora simples!\n\n")

print("Para começar, insira o primeiro número da operação: ")
n1 = input()

print("Em seguida, informe a operação desejada: ")
op = input()

print("Por fim, insira o segundo número da operação: ")
n2 = input()

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 1234

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(20)

sock.sendto(bytes(n1 + ' ' + op + ' ' + n2, 'utf-8'), (SERVER_HOST, SERVER_PORT))
try:
    response, address = sock.recvfrom(4096)
    code, return_msg = response.decode('utf-8').split(";")

    if(code == '0'):
        print("\nResposta recebida!")
        print(return_msg)
    elif(code == '1'):
        print("\nErro obtido: {s}".format(s=return_msg))
except:
    print("\nTempo de resposta excedido!")

sock.close()

