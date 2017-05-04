import cv2
from calibration_data import HSVData
from imutils.video import WebcamVideoStream, FPS
from image_processor import ESC_KEY
import argparse as ap


def calibrate_hsv(frames, src=0):
    hsv_data = HSVData()
    camera_stream = WebcamVideoStream(src=src).start()
    fps = FPS().start()

    while fps._numFrames < frames:
        frame = camera_stream.read()

        hsv_data.image = frame
        hsv_data.define_hsv_range()

    fps.stop()
    camera_stream.stop()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    arg_parser = ap.ArgumentParser()
    arg_parser.add_argument("-s", "--source", type=int, default=0, help="Source of the camera stream,"
                                                                        "by default it's the default webcam")
    arg_parser.add_argument("-n", "--num-frames", type=int, default=100, help="# of frames to read")
    args = vars(arg_parser.parse_args())
    calibrate_hsv(args["num_frames"], args["source"])
