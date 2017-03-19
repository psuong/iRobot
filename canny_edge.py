"""
Reference link: http://docs.opencv.org/trunk/da/d22/tutorial_py_canny.html
Reference for matplotlib sliders: http://matplotlib.org/api/widgets_api.html
Reference for Hough Transform: http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html
"""

import cv2
import numpy as np
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
            edged_image = self.edge_detect(image, 100, 200, True)
            # hough_image = self.hough_transform(image, edged_image)
            hough_pimage = self.probabilistic_hough_transform(image)

    def edge_detect(self, image: str, threshold1: float, threshold2: float, is_image_shown: bool = False):
        """
        Performs canny-edge detection on the image and returns it
        """
        img = cv2.imread(image, 0)
        edged_image = cv2.Canny(img, threshold1, threshold2)

        # Should the image be shown?
        if is_image_shown:
            plt.subplot(121), plt.imshow(img, cmap="gray")
            plt.title("Original Image"), plt.xticks([]), plt.yticks([])
            plt.subplot(122), plt.imshow(edged_image, cmap="gray")
            plt.title("Edged Image"), plt.xticks([]), plt.yticks([])
            plt.show()
        return edged_image

    def hough_transform(self, raw_image: str, edged_image: np.ndarray):
        img = cv2.imread(raw_image)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)

        lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
        print(lines)
        try:
            for line in lines:
                rho, theta = line[0]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * -b)
                y1 = int(y0 + 1000 * a)
                x2 = int(x0 - 1000 * -b)
                y2 = int(y0 - 1000 * -a)

                cv2.line(img, (x1, y2), (x2, y2), (0, 0, 255), 2)

            plt.subplot(121), plt.imshow(img, cmap="gray")
            plt.title("Hough Transform"), plt.xticks([]), plt.yticks([])
            plt.subplot(122), plt.imshow(edges, cmap="gray")
            plt.title("Edged Image"), plt.xticks([]), plt.yticks([])
            plt.show()
        except (Exception):
            pass

    def probabilistic_hough_transform(self, raw_image: str):
        img = cv2.imread(raw_image)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=1000, maxLineGap=100)
        try:
            for line in lines:
                x1, x2, y1, y2 = line[0]
                cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            plt.subplot(121), plt.imshow(img, cmap="gray")
            plt.title("Hough P Transform"), plt.xticks([]), plt.yticks([])
            plt.subplot(122), plt.imshow(edges, color="gray")
            plt.title("Edged Image"), plt.xticks([]), plt.yticks([])
            plt.show()
        except(Exception):
            print("Passed")
            pass


if __name__ == "__main__":
    # TODO: Run the function which performs the canny edge detection
    edge_detector = EdgeDetector()
    files = edge_detector.get_image_files("img")
    edge_detector.process_images(files)
