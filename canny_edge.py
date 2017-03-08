"""
Reference link: http://docs.opencv.org/trunk/da/d22/tutorial_py_canny.html
Reference for matplotlib sliders: http://matplotlib.org/api/widgets_api.html
Reference for Hough Transform: http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
"""

import cv2
import numpy
import os
from matplotlib import pyplot as plt


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

    def process_images(self, images: []):
        for image in images:
            self.edge_detect(image, 100, 200)

    def edge_detect(self, image: str, threshold1: float, threshold2: float):
        """
        Performs canny-edge detection on the image.
        """
        img = cv2.imread(image, 0)
        edges = cv2.Canny(img, threshold1, threshold2)

        print (type(edges))

        plt.subplot(121), plt.imshow(img, cmap="gray")
        plt.title("Original Image"), plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(edges, cmap="gray")
        plt.title("Edged Image"), plt.xticks([]), plt.yticks([])
        plt.show()

    def hough_transform(self, raw_image: str, edged_image: str):
        img = cv2.imread(image)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        pass


if __name__ == "__main__":
    # TODO: Run the function which performs the canny edge detection
    edge_detector = EdgeDetector()
    files = edge_detector.get_image_files("img")
    edge_detector.process_images(files)
