import os
from enum import Enum
from datetime import datetime

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
    def __init__(self, max_count=30, wait_time=2):
        """
        Constructor for the MotorManager class.
        :param max_count: How many iterations do we allow for sampling?
        :param wait_time: How many seconds should we make the rover wait?
        """
        self.origin_time = None
        self.movement_count = {
            Keys.KEY_UP: 0,
            Keys.KEY_LEFT: 0,
            Keys.KEY_RIGHT: 0,
            Keys.KEY_SPACE: 0
        }
        self.non_detected_count = 0
        self.max_count = max_count
        self.non_detected_threshold = max_count
        self.wait_time = 3

    def update_non_detected_count(self, funct, *args):
        """
        Every time the motor has passed the lane - we attempt to make the car turn
        :param funct: The function to execute
        :param args: The args of the function
        :return: 
        """
        self.non_detected_count += 1

        # Set hhe origin time for the counter
        if self.origin_time is None:
            self.origin_time = datetime.now()

        # If we have reached the threshold and the elapsed time is greater than our wait time...
        if self.non_detected_threshold > self.non_detected_threshold and \
            datetime.now().second - self.origin_time.second >= self.wait_time:
            self.non_detected_count = 0 # Reset the detected count
            self.origin_time = None
            funct(*args) # Execute the delegated function

    def update_movement(self, key):
        """
        Updates the movement depending on the key
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
