import socket, json


class Client:

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(3)

    def entrar(self, server_ip, server_port, nick):
        self.s.connect((server_ip, server_port))
        nick_dict = {'Comando': '/ENTRAR', 'Nick': nick}
        self.s.sendall(bytes(json.dumps(nick_dict), 'utf-8'))

    def enviarMensagem(self, msg):
        msg_dict = {'Comando': '/MENSAGEM', 'Mensagem': msg}
        self.s.sendall(bytes(json.dumps(msg_dict), 'utf-8'))

    def receberMensagem(self):
        try:
            msg = self.s.recv(4096)
            msg_json = msg.decode('utf-8')
            msg_dict = json.loads(msg_json)
            return msg_dict
        except:
            pass


    def listar(self):
        listar_dict = {'Comando': '/USUARIOS'}
        self.s.sendall(bytes(json.dumps(listar_dict), 'utf-8'))

    def sair(self):
        sair_dict = {'Comando': '/SAIR'}
        self.s.sendall(bytes(json.dumps(sair_dict), 'utf-8'))
        self.s.close()