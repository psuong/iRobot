from image_processor import FileManager, ImageProcessor, ESC_KEY
from camera import IMG_DIR, VIDEO_DIR, VideoReader, FRAME_SIZE
from calibration import calibrate_canny
import cv2
import numpy as np
from lane_tracking.detect import LaneDetector


def main():
    file_manager = FileManager()
    image_processor = ImageProcessor()


def image_process():
    file_manager = FileManager()
    # Hard coded the threshold values for the images
    image_processor = ImageProcessor(threshold_1=114, threshold_2=237)
    file_manager.get_image_files(IMG_DIR)


def video_process():
    image_processor = ImageProcessor(threshold_1=1000, threshold_2=2000)
    image_processor.aperture_size = 5
    # video = VideoReader("{}{}".format(VIDEO_DIR, "hough_transform_sample.mp4"))
    video = VideoReader("http://192.168.1.107:8080/?action=stream")

    capture = video.open_video()

    lane_detect = LaneDetector(50)

    while capture.isOpened():
        ret, frame = capture.read()

        image = frame

        height = frame.shape[0]
        width = frame.shape[1]

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edged_image = image_processor.edge_detect(gray)

        points = lane_detect.detect(image)

        if points is not None:
            if points[0] is not None and points[1] is not None:
                l_p1 = (int(points[0][0]), points[0][1])
                l_p2 = (int(points[0][2]), points[0][3])
                r_p1 = (int(points[1][0]), points[1][1])
                r_p2 = (int(points[1][2]), points[1][3])

                cv2.line(image, l_p1, l_p2, (0, 255, 0), 2)
                cv2.line(image, r_p1, r_p2, (0, 255, 0), 2)
        else:
            print(points)

        image = image_processor.horizontal_line(image, width, height)
        image = image_processor.vertical_line(image, width, height)

        # hough_transformed_image = image_processor.phough_transform(edged_image, frame)

        # cv2.imshow("Edged", edged_image)
        # cv2.imshow("Hough Transform", hough_transformed_image)
        cv2.imshow("", image)
        key = cv2.waitKey(ESC_KEY)

        if ESC_KEY == 27:
            break


if __name__ == "__main__":
    # main()
    video_process()
    # calibrate_canny("{}{}".format(VIDEO_DIR, "home_grown.webm"))
