import cv2
from calibration_data import HSVData, BlurData
from imutils.video import WebcamVideoStream, FPS
import argparse as ap


def calibrate_hsv(frames, path, src=0):
    hsv_data = HSVData()
    camera_stream = WebcamVideoStream(src=src).start()
    fps = FPS().start()

    while fps._numFrames < frames:
        frame = camera_stream.read()
        hsv_data.image = frame
        hsv_data.define_hsv_range()
        HSVData.serialize_hsv_data(hsv_data.lower_bound, hsv_data.upper_bound, path)

    fps.stop()
    camera_stream.stop()
    cv2.destroyAllWindows()


def calibrate_blur(frames, path, src=0):
    blur_data = BlurData()
    camera_stream = WebcamVideoStream(src=src).start()
    fps = FPS().start()

    while fps._numFrames < frames:
        frame = camera_stream.read()
        blur_data.image = frame
        blur_data.define_blur_strength()
        BlurData.serialize_blur_data(blur_data, path)

    fps.stop()
    camera_stream.stop()
    cv2.destroyAllWindows()


def main():
    arg_parser = ap.ArgumentParser()
    arg_parser.add_argument("-s", "--source", type=int, default=0, help="Source of the camera stream,"
                                                                        "by default it's the default webcam")
    arg_parser.add_argument("-n", "--num-frames", type=int, default=100, help="# of frames to read")
    arg_parser.add_argument("-p", "--path", type=str, help="File to write the data to")
    args = vars(arg_parser.parse_args())
    # calibrate_hsv(args["num_frames"], args["path"], args["source"])
    calibrate_blur(args["num_frames"], args["path"], args["source"])


if __name__ == "__main__":
    main()
