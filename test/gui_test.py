import matplotlib.pyplot as pyplot
from matplotlib.widgets import Slider, Button, RadioButtons
import numpy as np

class GUI(object):
    def __init__(self):
        self.figure, axis = pyplot.subplots()
        pyplot.subplots_adjust(left = 0.25, bottom = 0.25)
        self.t = np.arrange(0.0, 1.0, 0.001)


    