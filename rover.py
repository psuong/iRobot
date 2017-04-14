"""
Execute in Intel Edison
"""

import mraa
import time

DEFAULT_RUN_LENGTH = 0.3


class RoverClient(object):
    def __init__(self, left=(2, 3), right=(4, 5)):
        # GPIO pin setup
        self.left_backward = mraa.Gpio(left[0])
        self.left_forward = mraa.Gpio(left[1])

        self.right_forward = mraa.Gpio(right[0])
        self.right_backward = mraa.Gpio(right[1])

        self.left_forward.dir(mraa.DIR_OUT)
        self.left_backward.dir(mraa.DIR_OUT)
        self.right_backward.dir(mraa.DIR_OUT)
        self.right_forward.dir(mraa.DIR_OUT)

        self.halt()

    def halt(self):
        self.left_forward.write(0)
        self.left_backward.write(0)
        self.right_forward.write(0)
        self.right_backward.write(0)

    def on(self, *args):
        for arg in args:
            arg.write(1)

    def off(self, *args):
        for arg in args:
            arg.write(0)

    def nap(self, seconds=DEFAULT_RUN_LENGTH):
        time.sleep(seconds)

    def forward(self, seconds=DEFAULT_RUN_LENGTH):
        self.on(self.right_forward, self.left_forward)
        self.nap(seconds)
        self.off(self.right_forward, self.left_forward)

    def backward(self, seconds=DEFAULT_RUN_LENGTH):
        self.on(self.right_backward, self.left_backward)
        self.nap(seconds)
        self.off(self.right_backward, self.left_backward)

    def forward_right(self, seconds=DEFAULT_RUN_LENGTH):
        self.on(self.left_forward, self.right_backward)
        self.nap(seconds)
        self.off(self.left_forward, self.right_backward)

    def forward_left(self, seconds=DEFAULT_RUN_LENGTH):
        self.on(self.right_forward, self.left_backward)
        self.nap(seconds)
        self.off(self.right_forward, self.left_backward)
