"""
https://wiki.python.org/moin/UdpCommunication
"""

import socket


UDP_IP = '192.168.2.3'
UDP_PORT = 9000

# Move bytecodes
class Move(object):
    BACKWARD = b'$5'
    BACKWARD_LEFT = b'$7'
    BACKWARD_RIGHT = b'$6'
    FORWARD = b'$0'
    FORWARD_LEFT = b'$3'
    FORWARD_RIGHT = b'$4'
    LEFT = b'$8'
    RIGHT = b'$9'
    KEEP_ALIVE = b'$?'
    POWER = b'$!'

class RoverClient(object):
    def __init__(self, udp_ip=UDP_IP, udp_port=UDP_PORT):
        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.udp_pair = (self.udp_ip, self.udp_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, message):
        # Send a Move bytecode
        if not isinstance(message, bytes):
            message = message.encode('utf-8')
        self.sock.sendto(message, self.udp_pair)

    def connect_wifi(self):
        raise NotImplementedError()
