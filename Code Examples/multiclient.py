import socket

MCAST_GRP = '225.1.1.1'
MCAST_PORT = 1234
MULTICAST_TTL = 2

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, MULTICAST_TTL)
sock.sendto(bytes("robot", "utf-8"), (MCAST_GRP, MCAST_PORT))