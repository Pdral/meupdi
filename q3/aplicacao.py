import socket, objetos_pb2

SERVIDOR_IP = '127.0.0.1'
SERVIDOR_PORTA = 1234
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVIDOR_IP, SERVIDOR_PORTA))
print("Bem vindo ao gerenciamento de estufa!\n")
while True:
    print("Insira a opção desejada:")
    print("1 - ")