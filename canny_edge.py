"""
Reference link: http://docs.opencv.org/trunk/da/d22/tutorial_py_canny.html
"""

import cv2
import numpy
import os
from matplotlib import pyplot

class EdgeDetector(object):
    def __init__(self):
        self.__included_extension = [".png", ".jpg", ".jpeg"]
    def get_image_files(self, dir: str):
        image_files = [file for file in os.listdir(dir)
                       if any(file.endswith(extension) for extension in self.__included_extension)]
        return image_files

if __name__ == "__main__":
    # TODO: Run the function which performs the canny edge detection
    edge_detector = EdgeDetector()
    files = edge_detector.get_image_files("img")
    print (files)
