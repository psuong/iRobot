import os
import cv2
import math
from image_processor import ImageProcessor, ESC_KEY
from camera import VideoReader, VIDEO_DIR
from lane_tracking.detect import LaneDetector
from imutils.video import WebcamVideoStream
from thread_manager import ThreadManager
from remote_control import client
from remote_control.client import Keys
from calibration_data import HSVData, UPPER_BOUND, LOWER_BOUND, DATA_DIR, load_serialize_data


try:
    from rover import RoverClient

    rover = RoverClient()
    rover_status = True
except:
    rover_status = False

LIVE_STREAM = "http://192.168.1.118:8080/video"
image_processor = ImageProcessor(threshold_1=1000, threshold_2=2000)


def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return None

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return [int(x), int(y)]


def main(color_filter):
    if os.environ.get('VIDEO_PATH') is not None:
        camera_stream = WebcamVideoStream(src=LIVE_STREAM).start()
    else:
        camera_stream = WebcamVideoStream(src=1).start()

    window_name = "Main"

    lane_detect = LaneDetector(50)

    while camera_stream.stream.isOpened():
        frame = camera_stream.read()

        if frame is not None:
            height = frame.shape[0]
            width = frame.shape[1]

            image = ImageProcessor.filter_colors(frame, color_filter[LOWER_BOUND], color_filter[UPPER_BOUND])
            points = lane_detect.detect(image)

            if points is not None and points[0] is not None and points[1] is not None:
                l_p1 = (int(points[0][0]), int(points[0][1]))
                l_p2 = (int(points[0][2]), int(points[0][3]))
                r_p1 = (int(points[1][0]), int(points[1][1]))
                r_p2 = (int(points[1][2]), int(points[1][3]))

                # TODO: Store the coordinates of the lane

                cv2.line(image, l_p1, l_p2, (0, 255, 0), 2)
                cv2.line(image, r_p1, r_p2, (0, 255, 0), 2)

                left_lane = (l_p1, l_p2)
                right_lane = (r_p1, r_p2)

                vp = line_intersection(left_lane, right_lane)
                # If the VP exists
                if vp:
                    # Draw the theoretical vp
                    cv2.circle(image, tuple(vp), 10, (0, 244, 255), thickness=4)

                    warning_detection(height, width, image, vp, left_lane, right_lane)
            else:
                print("Passed")
                continue

            cv2.imshow(window_name, image)
            key = cv2.waitKey(ESC_KEY) & 0xFF
            if key == 27:
                break


def warning_detection(width, height, image, vp, left_lane, right_lane):
    half_width = int(width / 2)
    half_height = int(height / 2)

    bottom_left = (vp[0] - half_width, vp[1] + half_height)
    bottom_right = (vp[0] + half_width, vp[1] + half_height)

    cv2.rectangle(image,
                  (vp[0] - half_width, vp[1]),
                  (vp[0] + half_width, vp[1] + half_height),
                  (0, 0, 255), thickness=2)

    m = line_intersection((bottom_left, bottom_right), left_lane)
    s = line_intersection((bottom_left, bottom_right), right_lane)
    if m is not None and s is not None:
        a_m = m[0]
        b_m = m[1]
        a_s = s[0]
        b_s = s[1]

        # Draw the left distance of the screen
        cv2.line(image, tuple(m), bottom_left, (66, 244, 89), thickness=4)
        # Draw the intersection
        cv2.circle(image, tuple(m), radius=4, color=(66, 244, 89), thickness=5)
        # Draw the right distance of the screen
        cv2.line(image, tuple(s), bottom_right, (66, 244, 89), thickness=4)
        # Draw the intersection
        cv2.circle(image, tuple(s), radius=4, color=(66, 244, 89), thickness=5)


if __name__ == "__main__":
    color_filter_file = os.path.join(DATA_DIR, "white_table.p")
    color_filter_data = load_serialize_data(color_filter_file)

    main(color_filter_data)
