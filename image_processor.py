import cv2
import numpy as np
import os


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
    def __init__(self, threshold_1=None, threshold_2=None):
        self.threshold_1 = threshold_1 or 100
        self.threshold_2 = threshold_2 or 200
        self.aperture_size = 3
        self.points = {
            "mid_line": ((), ()), # Represents a pair of points
            "left_bound": (0, 0), # Left - a cartesian coordinate
            "right_bound": (0, 0) # Right - a cartesian coordinate
        }

    def set_raw_image(self, raw_image: np.ndarray):
        self.raw_image = raw_image

    def edge_detect(self, image: np.ndarray) -> np.ndarray:
        # self.set_raw_image(image)
        cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)
        self.edged_image = cv2.Canny(image, self.threshold_1, self.threshold_2, apertureSize=self.aperture_size)
        return self.edged_image

    def bilateral_blur(self, image: np.ndarray) -> np.ndarray:
        """
        Performs a bilateral blue to reduce noise
        :param image: Image to perform the blur on
        :return: The blurred image
        """
        pass

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


    def draw_horizontal_line(self, image: np.ndarray) -> np.ndarray:
        """
        Draws a horizontal line to represent the horizon
        :param image: The image to manipulate
        :return: The manipulated image
        """
        # print("L: {}, R: {}".format(self.points["left_bound"], self.points["right_bound"]))
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

    def phough_transform(self, edged_image: np.ndarray, image: np.ndarray) -> np.ndarray:
        lines = cv2.HoughLinesP(edged_image, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)
        if lines is None:
            return image
        for line in lines:
            x1, y1, x2, y2 = line[0][0], line[0][1], line[0][2], line[0][3]
            cv2.line(image, (x1, y1), (x2, y2), color=(66, 244, 69), thickness=6)

        # Draw horizontal lines
        return image

