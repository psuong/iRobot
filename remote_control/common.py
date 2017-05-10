import os
from enum import Enum

UDP_IP = os.environ.get('UDP_IP') or '192.168.43.164' or '127.0.0.1'
UDP_PORT = os.environ.get('UDP_PORT') or 5005

UDP_IP_PORT = (UDP_IP, UDP_PORT)


class Keys(Enum):
    """
    Key constants
    """
    KEY_UP = b'0'
    KEY_DOWN = b'1'
    KEY_RIGHT = b'2'
    KEY_LEFT = b'3'
    KEY_SPACE = b'4'
