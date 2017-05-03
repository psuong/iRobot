from __future__ import print_function
import cv2
from camera import VideoReader
from image_processor import ImageProcessor
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import argparse
import imutils
import numpy as np


def void_delegate(value: float):
    pass


def calibrate_canny(video_path):
    video_reader = VideoReader(video_path)
    video_reader.open_video()

    image_processor = ImageProcessor()

    generator = video_reader.read_video()

    for image, status in generator:
        window_name = "Edged Image"
        threshold1_name = "Threshold 1"
        threshold2_name = "Threshold 2"
        aperture_name = "Aperture Size"

        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

        # Create the
        cv2.createTrackbar(threshold1_name, window_name, image_processor.threshold_1, 1000, void_delegate)
        cv2.createTrackbar(threshold2_name, window_name, image_processor.threshold_2, 2000, void_delegate)
        cv2.createTrackbar(aperture_name, window_name, 3, 10, void_delegate)

        # edged_image = image_processor.edge_detect(image)
        while True:
            cv2.imshow(window_name, edged_image)

            image_processor.threshold_1 = cv2.getTrackbarPos(threshold1_name, window_name)
            image_processor.threshold_2 = cv2.getTrackbarPos(threshold2_name, window_name)
            image_processor.aperture_size = cv2.getTrackbarPos(aperture_name, window_name)

            edged_image = cv2.Canny(image, image_processor.threshold_1, image_processor.threshold_2,
                                    apertureSize=image_processor.aperture_size)

            key = cv2.waitKey(33)
            if key == 27:
                break
        cv2.destroyAllWindows()


def calibrate_hsv():
    hue1 = 0
    saturation1 = 0
    value1 = 0
    hue2 = 255
    saturation2 = 20
    value2 = 255

    video_reader = VideoReader(1)
    video_reader.open_video()

    # generator = video_reader.read_video()

    while video_reader.video.isOpened():
        ret, image = video_reader.video.read()

        cached_image = image

        cv2.namedWindow("", cv2.WINDOW_NORMAL)

        cv2.createTrackbar("HUE 1", "", hue1, 255, void_delegate)
        cv2.createTrackbar("SAT 1", "", saturation1, 255, void_delegate)
        cv2.createTrackbar("VAL 1", "", value1, 255, void_delegate)

        cv2.createTrackbar("HUE 2", "", hue2, 255, void_delegate)
        cv2.createTrackbar("SAT 2", "", saturation2, 255, void_delegate)
        cv2.createTrackbar("VAL 2", "", value2, 255, void_delegate)

        while True:
            hue1 = cv2.getTrackbarPos("HUE 1", "")
            saturation1 = cv2.getTrackbarPos("SAT 1", "")
            value1 = cv2.getTrackbarPos("VAL 1", "")

            hsv1 = np.array([hue1, saturation1, value1])

            hue2 = cv2.getTrackbarPos("HUE 2", "")
            saturation2 = cv2.getTrackbarPos("SAT 2", "")
            value2 = cv2.getTrackbarPos("VAL 2", "")

            hsv2 = np.array([hue2, saturation2, value2])

            image = ImageProcessor.filter_colors(cached_image, hsv1, hsv2)
            cv2.imshow("", image)
            key = cv2.waitKey(33)
            if key == 27:
                break

    cv2.destroyAllWindows()


def main_multi_threaded():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-n", "--num-frames", type=int, default=100)
    arg_parser.add_argument("-d", "--display", type=int, default=-1)
    args = vars(arg_parser.parse_args())

    camera_stream = WebcamVideoStream(src=0).start()
    fps = FPS().start()

    while fps._numFrames < args["num_frames"]:
        frame = camera_stream.read()
        frame = imutils.resize(frame, width=400)

        if args["display"] > 0:
            cv2.imshow("", frame)
            cv2.waitKey(1) & 0xFF

        fps.update()

    cv2.destroyAllWindows()
    camera_stream.stop()
    fps.stop()
    print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-n", "--num-frames", type=int, default=100)
    arg_parser.add_argument("-d", "--display", type=int, default=-1)
    args = vars(arg_parser.parse_args())

    camera_stream = VideoReader(0).open_video()
    fps = FPS().start()

    while fps._numFrames < args["num_frames"]:
        ret, frame = camera_stream.read()

        frame = imutils.resize(frame, width=400)

        if args["display"] > 0:
            cv2.imshow("", frame)
            cv2.waitKey(1) & 0xFF

        fps.update()

    cv2.destroyAllWindows()
    fps.stop()
    print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))


if __name__ == "__main__":
    # main()
    # main_multi_threaded()
    calibrate_hsv()