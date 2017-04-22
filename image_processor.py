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
        self.left_bound = (0, 0)
        self.right_bound = (0, 0)
        self.mid_point = (0, 0)

    def set_raw_image(self, raw_image: np.ndarray):
        self.raw_image = raw_image

    def edge_detect(self, image: np.ndarray) -> np.ndarray:
        # self.set_raw_image(image)
        cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)
        self.edged_image = cv2.Canny(image, self.threshold_1, self.threshold_2, apertureSize=self.aperture_size)
        return self.edged_image

    def horizontal_line(self, image, width, height):
        adjusted_height = int(2 * height / 3)
        adjusted_width = int(width / 2)
        self.left_bound = (0, adjusted_height)
        self.right_bound = (width, adjusted_height)
        self.mid_point = (adjusted_width, adjusted_height)
        cv2.line(image, self.left_bound, self.right_bound, (255, 0, 0), 2)
        return image

    def vertical_line(self, image, width, height):
        adjusted_height = int(height / 2)
        adjusted_width = int(width / 2)

        mid_high = (adjusted_width, adjusted_height)
        mid_low = (adjusted_width, height)

        cv2.line(image, mid_low, mid_high, (255, 0, 0), 2)
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

