"""
Reference link: http://docs.opencv.org/trunk/da/d22/tutorial_py_canny.html
Reference for matplotlib sliders: http://matplotlib.org/api/widgets_api.html
"""

import cv2
import numpy
import os
from matplotlib import pyplot as plt
# TODO: Import the sliders

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
        for image in images:
            img = cv2.imread(image, 0);
            # TODO: Add sliders to manipulate the canny edge detection values
            edges = cv2.Canny(img, 100, 200)

            plt.subplot(121), plt.imshow(img, cmap="gray")
            plt.title("Original Image"), plt.xticks([]), plt.yticks([])
            plt.subplot(122), plt.imshow(edges, cmap="gray")
            plt.title("Edge Image"), plt.xticks([]), plt.yticks([])

            plt.show()


if __name__ == "__main__":
    # TODO: Run the function which performs the canny edge detection
    edge_detector = EdgeDetector()
    files = edge_detector.get_image_files("img")
    edge_detector.edge_detect_images(files)
