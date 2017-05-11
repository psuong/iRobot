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


class MotorManager(object):
    def __init__(self, max_count=30):
        self.movement_count = {
            Keys.KEY_UP: 0,
            Keys.KEY_LEFT: 0,
            Keys.KEY_RIGHT: 0,
            Keys.KEY_SPACE: 0
        }
        self.max_count = max_count

    def update_movement(self, key):
        """
        Updates the movement.
        :param key: Movement key
        :return: None
        """
        self.movement_count[key] += 1

    def reset_movement(self):
        """
        Resets the dictionary which has the movement
        :return: None
        """
        for key in self.movement_count.keys():
            self.movement_count[key] = 0

    def get_max_movement(self):
        """
        Returns the majority movement key
        :return: Key, Value
        """
        value, key = max((value, key) for key, value in self.movement_count.items())
        return key
