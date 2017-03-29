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
    def __init__(self, show_image=False):
        self.threshold_1 = 100
        self.threshold_2 = 200
        self.aperture_size = 3
        self.show_image = show_image
        # Image fields
        self.raw_image = None
        self.edged_image = None
        self.hough_transformed_image = None

    def set_raw_image(self, raw_image: np.ndarray):
        self.raw_image = raw_image

    def edge_detect(self, image: np.ndarray) -> np.ndarray:
        # img = cv2.imread(image)
        self.set_raw_image(image)
        cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)
        self.edged_image = cv2.Canny(image, self.threshold_1, self.threshold_2, apertureSize=self.aperture_size)

        if self.show_image:
            window_name = "Edged Image"
            threshold1_name = "Threshold 1"
            threshold2_name = "Threshold 2"
            aperture_name = "Aperture Size"
            cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
            cv2.imshow(window_name, self.edged_image)

            # Create the trackbars
            cv2.createTrackbar(threshold1_name, window_name, 100, 1000, void_delegate)
            cv2.createTrackbar(threshold2_name, window_name, 200, 2000, void_delegate)
            cv2.createTrackbar(aperture_name, window_name, 3, 10, void_delegate)

            while 1:
                cv2.imshow(window_name, self.edged_image)
                k = cv2.waitKey(ESC_KEY) # Press the escape key to exit the application

                if k == 27:
                    break

                self.threshold_1 = cv2.getTrackbarPos(threshold1_name, window_name)
                self.threshold_2 = cv2.getTrackbarPos(threshold2_name, window_name)
                self.aperture_size = cv2.getTrackbarPos(aperture_name, window_name)

                self.edged_image = cv2.Canny(img, self.threshold_1, self.threshold_2, apertureSize=3)
            cv2.destroyAllWindows()
        return self.edged_image

    # TODO: Fix the raw_image setting when performing a hough_transform
    def phough_transform(self, edged_image: np.ndarray) -> np.ndarray:
        gray_scaled_image = cv2.cvtColor(self.raw_image, cv2.COLOR_BGR2GRAY)
        lines = cv2.HoughLinesP(edged_image, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)
        try:
            for x1, y1, x2, y2 in lines[0]:
                cv2.line(gray_scaled_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

            print("Writing an image")
            cv2.imwrite("hough_transformed_image.jpeg", gray_scaled_image)
        except(Exception):
            pass

        if self.show_image:
            window_name = "Hough Transform"
            min_line_name = "Min Line Length"
            max_line_name = "Max Line Gap"
            cv2.namedWindow(window_name)
            cv2.imshow(window_name, gray_scaled_image)

            # Create the trackbars
            # cv2.createTrackbar(min_line_name, window_name, 100, 1000, void_delegate)
            # cv2.createTrackbar(max_line_name, window_name, 200, 2000, void_delegate)

            while 1:
                cv2.imshow(window_name, gray_scaled_image)
                k = cv2.waitKey(ESC_KEY)

                if k == 27:
                    break
