import cv2
from calibration_data import HSVData
from imutils.video import WebcamVideoStream
import argparse as ap


def calibrate_hsv(src=0):
    hsv_data = HSVData()
    camera_stream = WebcamVideoStream(src=src).start()

    while True:
        frame = camera_stream.read()

        hsv_data.image = frame
        hsv_data.define_hsv_range()


if __name__ == "__main__":
    arg_parser = ap.ArgumentParser()
    arg_parser.add_argument("-s", "--source", type=int, default=0, help="Source of the camera stream,"
                                                                        "by default it's the default webcam")
    args = vars(arg_parser.parse_args())
    calibrate_hsv(args["source"])
