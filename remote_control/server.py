import socket

from .common import UDP_IP_PORT

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
sock.bind(UDP_IP_PORT)

while True:
    data, addr = sock.recvfrom(1024)
    print("recieved ", data, addr)