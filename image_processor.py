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

    def set_raw_image(self, raw_image: np.ndarray):
        self.raw_image = raw_image

    def edge_detect(self, image: np.ndarray) -> np.ndarray:
        # self.set_raw_image(image)
        cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)
        self.edged_image = cv2.Canny(image, self.threshold_1, self.threshold_2, apertureSize=self.aperture_size)
        return self.edged_image

    def phough_transform(self, edged_image: np.ndarray, image: np.ndarray) -> np.ndarray:
        lines = cv2.HoughLinesP(edged_image, 1, np.pi/180, 100, minLineLength=10, maxLineGap=10)
        if lines is None:
            return None
        for x1, y1, x2, y2 in lines[0]:
            cv2.line(image, (x1, y1), (x2, y2), color=(66, 244, 69), thickness=6)
        return image

