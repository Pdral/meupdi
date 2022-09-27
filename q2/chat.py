import threading, time, sys
from cliente import Client

sair = False
cliente = Client()
msgs = []

def interface():
    while True:
        print("Você pode escrever uma mensagem ou utilizar um dos comandos abaixo:")
        print("/USUARIOS, /SAIR")
        msg = input()
        if msg == '/USUARIOS':
            cliente.listar()
        elif msg == '/SAIR':
            sair = True
            time.sleep(3)
            cliente.sair()
            print('Você foi desconectado do chat')
            break
        else:
            cliente.enviarMensagem(msg)
            print("Mensagem enviada com sucesso!")
        print()
        time.sleep(3)


def recebeMensagem():
    while True:
        if sair: break
        msg_dict = cliente.receberMensagem()
        if msg_dict is not None:
            if msg_dict['Tipo'] == 0:
                msg = msg_dict['Conteúdo']
                msgs.append(msg)
                print("Uma mensagem foi recebida!")
                print('CHAT:')
                if len(msgs) > 4:
                    lista = msgs[-5:]
                else:
                    lista = msgs
                for mensagem in lista:
                    print(mensagem)
            else:
                print("Lista de usuários:")
                for user in msg_dict['Conteúdo']: print(user)
            print()


HOST = 'localhost'
PORT = 1234

print("Bem vindo ao chat!")
print("Para começar, informe seu nickname: ")
nick = input()
cliente.entrar(HOST, PORT, nick)
print("Conectado com sucesso!\n")
t1 = threading.Thread(target=recebeMensagem)
t2 = threading.Thread(target=interface)
t1.start()
t2.start()
while t1.is_alive() and t2.is_alive(): pass
print("Aquicabou")
sys.exit()
