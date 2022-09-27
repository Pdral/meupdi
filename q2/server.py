import socket, json, threading

users = []


def client_thread(connection):
    data = connection.recv(4096)
    data_json = data.decode('utf-8')
    data_dict = json.loads(data_json)
    nick = data_dict['Nick']
    users.append((nick, connection))
    while True:
        data = connection.recv(4096)
        data_json = data.decode('utf-8')
        data_dict = json.loads(data_json)
        command = data_dict['Comando']
        if command == '/MENSAGEM':
            msg = data_dict['Mensagem']
            complete_msg = nick + ': ' + msg
            msg_dict = {'Tipo': 0, 'Conteúdo': complete_msg}
            msg_json = json.dumps(msg_dict)
            msg_bytes = bytes(msg_json, 'utf-8')
            for _, user_conn in users:
                user_conn.sendall(msg_bytes)
        elif command == '/USUARIOS':
            users_dict = {'Tipo': 1, 'Conteúdo': [user[0] for user in users]}
            users_json = json.dumps(users_dict)
            connection.sendall(bytes(users_json, 'utf-8'))
        elif command == '/SAIR':
            msg = '{name} saiu'.format(name=nick)
            msg_dict = {'Tipo': 0, 'Conteúdo': msg}
            msg_json = json.dumps(msg_dict)
            connection.sendall(bytes(msg_json, 'utf-8'))
            break


HOST = 'localhost'
PORT = 1234
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen()
while True:
    conn, addr = sock.accept()
    t = threading.Thread(target=client_thread(conn))
    t.start()

