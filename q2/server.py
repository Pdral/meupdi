import socket, json, threading

users = []


def client_thread(connection):
    try:
        data = connection.recv(4096)
    except:
        return
    data_json = data.decode('utf-8')
    data_dict = json.loads(data_json)
    try:
        nick = data_dict['Nick']
    except:
        return
    users.append((nick, connection))
    msg = '{s} entrou'.format(s=nick)
    msg_dict = {'Tipo': 0, 'Conteúdo': msg}
    msg_json = json.dumps(msg_dict)
    for _, connec in users:
        try:
            connec.sendall(bytes(msg_json, 'utf-8'))
        except:
            pass
    while True:
        try:
            data = connection.recv(4096)
        except:
            break
        data_json = data.decode('utf-8')
        data_dict = json.loads(data_json)
        try:
            command = data_dict['Comando']
        except:
            command = ''
        if command == '/MENSAGEM':
            try:
                msg = data_dict['Mensagem']
                complete_msg = nick + ': ' + msg
                msg_dict = {'Tipo': 0, 'Conteúdo': complete_msg}
                msg_json = json.dumps(msg_dict)
                msg_bytes = bytes(msg_json, 'utf-8')
                for _, user_conn in users:
                    try:
                        user_conn.sendall(msg_bytes)
                    except:
                        pass
            except:
                pass
        elif command == '/USUARIOS':
            users_dict = {'Tipo': 1, 'Conteúdo': [user[0] for user in users]}
            users_json = json.dumps(users_dict)
            try:
                connection.sendall(bytes(users_json, 'utf-8'))
            except:
                break
        elif command == '/SAIR':
            break
    msg = '{name} saiu'.format(name=nick)
    msg_dict = {'Tipo': 0, 'Conteúdo': msg}
    msg_json = json.dumps(msg_dict)
    users.remove((nick, connection))
    for _, connec in users:
        try:
            connec.sendall(bytes(msg_json, 'utf-8'))
        except:
            pass


HOST = 'localhost'
PORT = 1234
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen()
while True:
    conn, addr = sock.accept()
    t = threading.Thread(target=client_thread, args=(conn,), daemon=True)
    t.start()

