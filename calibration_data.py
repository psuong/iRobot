import pickle
import cv2
import numpy as np
from image_processor import ImageProcessor


def void_delegate(value):
    """
    Represents a void delegate that does absolutely nothing.
    :param value: Value from the trackbar
    :return: None
    """
    return None


class HSVData(object):
    """
    Stores the upper and lower bound of an HSV color picker. This helps
    reduce the noise of the image.
    
    Convenience functions will exist to show the data
    """
    def __init__(self, image):
        self.lower_bound = np.array([0, 0, 0])
        self.upper_bound = np.array([0, 0, 0])
        # Data range 1 (lower bound)
        self.hue_1 = 0
        self.saturation_1 = 0
        self.value_1 = 0
        # Data range 2 (upper bound)
        self.hue_2 = 0
        self.saturation_2 = 0
        self.value_2 = 0
        # Image data
        self.image = self.image
        # Represents the max range between 0 and the defined value
        self._max_range = 255

    def define_hsv_range(self):
        # Perform the manipulation on the cached image, keep the original image intact
        cached_image = self.image

        window_name = "HSV_Calibration"

        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.createTrackbar("Hue 1", window_name, self.hue_1, self._max_range, void_delegate)
        cv2.createTrackbar("Saturation 1", window_name, self.saturation_1, self._max_range, void_delegate)
        cv2.createTrackbar("Value 1", window_name, self.value_1, self._max_range, void_delegate)

        cv2.createTrackbar("Hue 1", window_name, self.hue_1, self._max_range, void_delegate)
        cv2.createTrackbar("Saturation 1", window_name, self.saturation_1, self._max_range, void_delegate)
        cv2.createTrackbar("Value 1", window_name, self.value_1, self._max_range, void_delegate)

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

            key = cv2.waitKey(33) & 0xFF

            if key == 27:
                break

        cv2.destroyAllWindows()
