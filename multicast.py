import socket

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007
msg = 'Paulo!!!!!!!!!'
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((MCAST_GRP, MCAST_PORT))
sock.sendto(bytes(msg, 'utf-8'), (MCAST_GRP, MCAST_PORT))
while True:
    print("Entrei")
    print(sock.recvfrom(10240)[0].decode('utf-8'))
sock.close()
