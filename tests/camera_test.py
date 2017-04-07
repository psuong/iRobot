import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import cv2
import camera


def test_video_reader(filename):
    print("Opening reader")
    vr = camera.VideoReader(filename)
    vr.open_video()
    read_generator = vr.read_video()
    img, status = next(read_generator)
    print("Got status ", status)
    cv2.imshow("Video Reader Test", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    command, filename = int(sys.argv[1]), sys.argv[2]
    print("Got ", command, filename)
    if command == 0:
        print("Executing ", 0)
        test_video_reader(filename)
