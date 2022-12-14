import socket

# Iniciando o servidor e seu socket
id = 0
HOST = '127.0.0.1'
PORT = 1234
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))
operacoes = ['+', '-', '*', '/']

# Loop para receber requisições
while True:
    id += 1
    print("Aguardando requisição de número {s} ...".format(s=id))
    data, address = sock.recvfrom(4096)
    msg = data.decode('utf-8')
    code = '1'
    return_msg = ""

    # Conversão da mensagem para os tipos apropriados
    msg_operacao = msg.split()

    if(len(msg_operacao) < 3):
        return_msg = "Elementos não podem ser nulos!"
    else:
        try:
            operador = msg_operacao[1]
            num1 = float(msg_operacao[0])
            num2 = float(msg_operacao[2])

            if(operador not in operacoes):
                return_msg = "Operador inválido!"

            elif operador == "/" and num2 == 0:
                return_msg = "Não é possível realizar divisão por 0"

            # Computação da operação requisitada
            else:
                resultado = 0

                if operador == '+':
                    resultado = num1 + num2
                elif operador == "-":
                    resultado = num1 - num2
                elif operador == "*":
                    resultado = num1 * num2
                elif operador == "/":
                    resultado = num1 / num2

                return_msg = "{a} {op} {b} = {s}".format(a=num1, op=operador, b=num2, s=resultado)
                code = '0'
        except ValueError as error:
            return_msg = error.args[0]

    sock.sendto(bytes(code + ';' + return_msg, 'utf-8'), address)
    print("Requisição de id {s} processada com sucesso!".format(s=id))



