"""
Execute in Intel Edison
"""

from utility import does_module_exists
import time


MODULE_NAME = "mraa"
DEFAULT_RUN_LENGTH = 0.5
DEFAULT_TURN_SLEEP = 0.3


if does_module_exists(MODULE_NAME):
    import mraa


class RoverClient(object):
    def __init__(self, left=(2, 3), right=(4, 5), pwm=(6, 9)):
        # GPIO pin setup
        if does_module_exists(MODULE_NAME):
            self.left_backward = mraa.Gpio(left[0])
            self.left_forward = mraa.Gpio(left[1])

            self.right_forward = mraa.Gpio(right[0])
            self.right_backward = mraa.Gpio(right[1])

            self.left_forward.dir(mraa.DIR_OUT)
            self.left_backward.dir(mraa.DIR_OUT)
            self.right_backward.dir(mraa.DIR_OUT)
            self.right_forward.dir(mraa.DIR_OUT)

            self.en_A = mraa.Pwm(pwm[1])
            self.en_B = mraa.Pwm(pwm[0])
    
            self.halt()
            self.en_A.write(.5)
            self.en_B.write(.5)

    def halt(self):
        if does_module_exists(MODULE_NAME):
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
        if does_module_exists(MODULE_NAME):
            self.on(self.right_forward, self.left_forward)
            self.nap(seconds)
            self.off(self.right_forward, self.left_forward)

    def backward(self, seconds=DEFAULT_RUN_LENGTH):
        if does_module_exists(MODULE_NAME):
            self.on(self.right_backward, self.left_backward)
            self.nap(seconds)
            self.off(self.right_backward, self.left_backward)

    def forward_right(self, seconds=DEFAULT_RUN_LENGTH):
        if does_module_exists(MODULE_NAME):
            self.on(self.left_forward, self.right_backward)
            self.nap(seconds)
            self.off(self.left_forward, self.right_backward)

    def forward_left(self, seconds=DEFAULT_RUN_LENGTH):
        if does_module_exists(MODULE_NAME):
            self.on(self.right_forward, self.left_backward)
            self.nap(seconds)
            self.off(self.right_forward, self.left_backward)
