# LINK PARA O VÍDEO: https://www.youtube.com/watch?v=C0R5KZZSAj8

from socket import *

nomeServidor = "localhost"
portaServidor = 8080
socketCliente = socket(AF_INET, SOCK_DGRAM) # AF_INET = IPv4 e SOCK_DGRAM = UDP
while True:
    numero = input('Tente adivinhar meu número secreto (1 a 10): ')
    numeroBytes = bytes(numero, 'UTF-8')
    socketCliente.sendto(numeroBytes, (nomeServidor,portaServidor))
    respostaBytes, enderecoServidor = socketCliente.recvfrom(2048)
    resposta = respostaBytes.decode('UTF-8')
    print(resposta)
    if resposta == 'Parabéns! Você acertou!':
        socketCliente.close()
        break

