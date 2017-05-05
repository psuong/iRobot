import pickle
import cv2
import os
import numpy as np
from image_processor import ImageProcessor

LOWER_BOUND = "lower"
UPPER_BOUND = "upper"
DATA_DIR = "serialized_data"


def void_delegate(value):
    """
    Represents a void delegate that does absolutely nothing.
    :param value: Value from the trackbar
    :return: None
    """
    return None


def load_serialize_data(path: str):
    """
    Loads the serialized data from a pickle dump
    :param path: Path to the file
    :return: Loaded data
    """
    file = open(path, "rb")
    serialized_data = pickle.load(file)
    file.close()
    return serialized_data


class HSVData(object):
    """
    Stores the upper and lower bound of an HSV color picker. This helps
    reduce the noise of the image.
    
    Convenience functions will exist to show the data
    """
    def __init__(self):
        # Represents the max range between 0 and the defined value
        self._max_range = 255

        self.lower_bound = np.array([0, 0, 0])
        self.upper_bound = np.array([0, 0, 0])
        # Data range 1 (lower bound)
        self.hue_1 = 0
        self.saturation_1 = 0
        self.value_1 = 0
        # Data range 2 (upper bound)
        self.hue_2 = self._max_range
        self.saturation_2 = self._max_range
        self.value_2 = self._max_range
        # Image data
        self.image = None

    def define_hsv_range(self):
        # Perform the manipulation on the cached image, keep the original image intact
        cached_image = self.image
        window_name = "HSV_Calibration"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

        cv2.createTrackbar("Hue 1", window_name, self.hue_1, self._max_range, void_delegate)
        cv2.createTrackbar("Saturation 1", window_name, self.saturation_1, self._max_range, void_delegate)
        cv2.createTrackbar("Value 1", window_name, self.value_1, self._max_range, void_delegate)

        cv2.createTrackbar("Hue 2", window_name, self.hue_2, self._max_range, void_delegate)
        cv2.createTrackbar("Saturation 2", window_name, self.saturation_2, self._max_range, void_delegate)
        cv2.createTrackbar("Value 2", window_name, self.value_2, self._max_range, void_delegate)

        while True:
            self.hue_1 = cv2.getTrackbarPos("Hue 1", window_name)
            self.saturation_1 = cv2.getTrackbarPos("Saturation 1", window_name)
            self.value_1 = cv2.getTrackbarPos("Value 1", window_name)
            self.lower_bound = np.array([self.hue_1, self.saturation_1, self.value_1])

            self.hue_2 = cv2.getTrackbarPos("Hue 2", window_name)
            self.saturation_2 = cv2.getTrackbarPos("Saturation 2", window_name)
            self.value_2 = cv2.getTrackbarPos("Value 2", window_name)
            self.upper_bound = np.array([self.hue_2, self.saturation_2, self.value_2])

            cached_image = ImageProcessor.filter_colors(self.image, self.lower_bound, self.upper_bound)

            cv2.imshow(window_name, cached_image)

            key = cv2.waitKey(33)

            if key == 27:
                break

        cv2.destroyAllWindows()

    @staticmethod
    def serialize_hsv_data(lower_bound: np.ndarray, upper_bound: np.ndarray, path: str):
        bounds = {
            LOWER_BOUND: lower_bound,
            UPPER_BOUND: upper_bound
        }
        data_path = os.path.join(DATA_DIR, path)
        output = open(data_path, "wb")
        pickle.dump(bounds, output)
        output.close()


class BlurData(object):
    def __init__(self):
        self.kernel_size = 5
        self.point = 5
        self.image = None
        self._max_range = 100

    def define_blur_strength(self):
        window_name = "Blur"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.createTrackbar("Kernel Size", window_name, self.kernel_size, self._max_range, void_delegate)
        cv2.createTrackbar("Point Size", window_name, self.point, self._max_range, void_delegate)

        while True:
            self.kernel_size = cv2.getTrackbarPos("Kernel Size", window_name)
            self.point = cv2.getTrackbarPos("Point Size", window_name)

            if self.kernel_size < 2:
                self.kernel_size = 2
            if self.point < 2:
                self.point = 2

            cached_image = cv2.blur(self.image, (self.kernel_size, self.point))
            cv2.imshow(window_name, cached_image)

            key = cv2.waitKey(33)
            if key == 27:
                break

    @staticmethod
    def serialize_blur_data(blur_data, path):
        data_path = os.path.join(DATA_DIR, path)
        output = open(data_path, "wb")
        pickle.dump(blur_data, output)
        output.close()
