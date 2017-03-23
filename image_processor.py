import cv2
import numpy as np
import os


def void_delegate(value: float):
    pass


class FileManager(object):
    def __init__(self):
        self.__included_extensions = [".png", ".jpg", ".jpeg"]

    def get_image_files(self, dir: str) -> []:
        image_files = []
        for file in os.listdir(dir):
            for extension in self.__included_extensions:
                if file.endswith(extension):
                    image_files.append("{}{}{}".format(dir, os.sep, file))
        return image_files

class ImageProcessor(object):
    def __init__(self, gui=None):
        self.threshold_1 = 100
        self.threshold_2 = 200
        self.aperture_size = 3
        self.gui_object = None

    def set_threshold_1(self, value: float):
        self.threshold_1 = value

    def set_threshold_2(self, value: float):
        self.threshold_2 = value

    def edge_detect(self, image: str, show_image: bool = True):
        img = cv2.imread(image)
        edged_image = cv2.Canny(img, self.threshold_1, self.threshold_2, apertureSize=self.aperture_size)
        cv2.threshold(edged_image, 128, 255, cv2.THRESH_BINARY_INV)

        if show_image:
            window_name = "Edged Image"
            threshold1_name = "Threshold 1"
            threshold2_name = "Threshold 2"
            aperture_name = "Aperture Size"
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            cv2.imshow(window_name, edged_image)

            # Create the trackbars
            cv2.createTrackbar(threshold1_name, window_name, 100, 1000, void_delegate)
            cv2.createTrackbar(threshold2_name, window_name, 200, 2000, void_delegate)
            cv2.createTrackbar(aperture_name, window_name, 3, 10, void_delegate)

            while True:
                cv2.imshow(window_name, edged_image)
                k = cv2.waitKey(0)

                self.threshold_1 = cv2.getTrackbarPos(threshold1_name, window_name)
                self.threshold_2 = cv2.getTrackbarPos(threshold2_name, window_name)
                self.aperture_size = cv2.getTrackbarPos(aperture_name, window_name)

                edged_image = cv2.Canny(img, self.threshold_1, self.threshold_2, apertureSize=self.aperture_size)

        return edged_image
