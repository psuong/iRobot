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
        image_files = []
        for file in os.listdir(dir):
            for extension in self.__included_extension:
                if file.endswith(extension):
                    image_files.append("{}{}{}".format(dir, os.sep, file))
        return image_files

    def edge_detect_images(self, images: []):
        pass

if __name__ == "__main__":
    # TODO: Run the function which performs the canny edge detection
    edge_detector = EdgeDetector()
    files = edge_detector.get_image_files("img")
    print (files)
