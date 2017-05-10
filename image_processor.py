import cv2
import numpy as np
import os
from lane_tracking.detect import LaneDetector

ESC_KEY = 33


def void_delegate(value: float):
    pass


class FileManager(object):
    def __init__(self):
        self.__included_extensions = [".png", ".jpg", ".jpeg"]

    def get_image_files(self, directory: str) -> []:
        image_files = []
        for file in os.listdir(directory):
            for extension in self.__included_extensions:
                if file.endswith(extension):
                    image_files.append("{}{}{}".format(directory, os.sep, file))
        return image_files


class ImageProcessor(object):
    def __init__(self, threshold_1=None, threshold_2=None, horizon=50):
        self.threshold_1 = threshold_1 or 100
        self.threshold_2 = threshold_2 or 200
        self.aperture_size = 3
        self.points = {
            "mid_line": ((), ()),  # Represents a pair of points
            "left_bound": (0, 0),  # Left - a cartesian coordinate
            "right_bound": (0, 0),  # Right - a cartesian coordinate,
            "lane_1": ((0, 0), (0, 0)),
            "lane_2": ((0, 0), (0, 0))
        }
        self.image = None

    @staticmethod
    def bilateral_blur(image: np.ndarray, queue=None) -> np.ndarray:
        """
        Performs a bilateral blue to reduce noise
        :param image: Image to perform the blur on
        :param queue: The queue to store the image into
        :return: The blurred image
        """
        blurred_image = cv2.bilateralFilter(image, 20, 100, 100)
        if queue is not None:
            queue.put(blurred_image)
        return blurred_image

    def find_points(self, width, height) -> None:
        """
        Computes the midpoints and the points on the extremities
        :param width: width of the image
        :param height: height of the image
        :return: 
        """
        adjust_height = int(height / 2)
        adjust_width = int(width / 2)
        left_bound = (0, int(2 * height / 3))
        right_bound = (width, int(2 * height / 3))
        mid_high = (adjust_width, adjust_height)
        mid_low = (adjust_width, height)

        self.points["mid_line"] = (mid_high, mid_low)
        self.points["left_bound"] = left_bound
        self.points["right_bound"] = right_bound

    def update_lanes(self, lane_1, lane_2):
        self.points["lane_1"] = lane_1
        self.points["lane_2"] = lane_2

    def draw_horizontal_line(self, image: np.ndarray) -> np.ndarray:
        """
        Draws a horizontal line to represent the horizon
        :param image: The image to manipulate
        :return: The manipulated image
        """
        cv2.line(image, self.points["left_bound"], self.points["right_bound"], (255, 0, 0), 2)
        return image

    def draw_midpoint_line(self, image: np.ndarray) -> np.ndarray:
        """
        Draws the perceived center of the image, this supposedly represents the middle of the road.
        :param image: The image to manipulate
        :return: the manipulated image
        """
        cv2.line(image, self.points["mid_line"][0], self.points["mid_line"][1], (255, 0, 0), 2)
        return image

    @staticmethod
    def filter_colors(image: np.ndarray, lower_bound, upper_bound):
        # https://pythonprogramming.net/color-filter-python-opencv-tutorial/
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        return cv2.bitwise_and(image, image, mask=mask)

