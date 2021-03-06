import os
import cv2
import math
import random
from image_processor import ImageProcessor, ESC_KEY
from lane_tracking.detect import LaneDetector
from imutils.video import WebcamVideoStream
from remote_control import client
from remote_control.common import MotorManager
from remote_control.client import Keys
from calibration_data import HSVData, UPPER_BOUND, LOWER_BOUND, DATA_DIR, load_serialize_data
from utility import line_intersection, distance, get_average_line
from lane_tracking.track import LaneTracker
from datetime import datetime

from remote_control import client, common


try:
    from rover import RoverClient

    rover = RoverClient()
    rover_status = True
except:
    rover_status = False

LIVE_STREAM = "http://192.168.43.164:8080/?action=stream"
image_processor = ImageProcessor(threshold_1=1000, threshold_2=2000)


def main():
    if os.environ.get('VIDEO_PATH') is None:
        camera_stream = WebcamVideoStream(src=LIVE_STREAM).start()
    else:
        camera_stream = WebcamVideoStream(src=1).start()

    window_name = "Main"

    lane_detect = LaneDetector(50)
    lane_tracker = LaneTracker(2, 0.1, 500)

    ticks = 0

    # Create the motor manager
    motor_manager = MotorManager(1)

    # Initialize the current iteration to 0
    current_iteration = 0

    # Create the start time
    start_time = None

    while camera_stream.stream.isOpened():
        pre_ticks = ticks
        ticks = cv2.getTickCount()
        dt = (ticks - pre_ticks) / cv2.getTickFrequency()

        frame = camera_stream.read()

        if frame is not None:
            height = frame.shape[0]
            width = frame.shape[1]

            image = frame
            predicted_points = lane_tracker.predict(dt)
            points = lane_detect.detect(image)

            if predicted_points is not None:
                cv2.line(image,
                         (predicted_points[0][0], predicted_points[0][1]),
                         (predicted_points[0][2], predicted_points[0][3]),
                         (255, 0, 0), 4)
                cv2.line(image,
                         (predicted_points[1][0], predicted_points[1][1]),
                         (predicted_points[1][2], predicted_points[1][3]),
                         (255, 0, 0), 4)

            if points is not None and points[0] is not None and points[1] is not None:
                lane_tracker.update(points)

                l_p1 = (int(points[0][0]), int(points[0][1]))
                l_p2 = (int(points[0][2]), int(points[0][3]))
                r_p1 = (int(points[1][0]), int(points[1][1]))
                r_p2 = (int(points[1][2]), int(points[1][3]))

                # Create the lanes
                left_lane, right_lane = LaneDetector.get_left_right_lanes((l_p1, l_p2), (r_p1, r_p2))

                # TODO: Store the coordinates of the lane
                # Draw the lanes
                cv2.line(image, left_lane[0], left_lane[1], (0, 255, 0), 2)
                cv2.line(image, right_lane[0], right_lane[1], (0, 255, 0), 2)

                vp = line_intersection(left_lane, right_lane)
                # If the VP exists
                if vp:
                    # Draw the theoretical vp
                    cv2.circle(image, tuple(vp), 10, (0, 244, 255), thickness=4)

                    dm_ds = warning_detection(height, width, image, vp, left_lane, right_lane)

                    # Get the movement
                    movement = perceive_movement(dm_ds[0], dm_ds[1], width / 4)
                    current_iteration += 1
                    # Sample a certain number of frames and grab the majority direction
                    if current_iteration <= motor_manager.max_count:
                        # Update the movement
                        motor_manager.update_movement(movement)
                    else:
                        # print("Start Time: ", start_time)
                        if start_time is None:
                            start_time = datetime.now()
                            # TODO: Time stamp how often we receive an instruction
                            # Reset the current iteration and update the movement
                            current_iteration = 0
                            motor_manager.update_movement(movement)
                            movement_key = motor_manager.get_max_movement()
                            motor_manager.reset_movement()
                            client.handle_key(Keys.KEY_SPACE)
                            print("-----------------Sending movement...-------------------")
                            # Send the movement to the rover
                            client.handle_key(movement_key)
                        if abs(datetime.now().second - start_time.second) > 2:
                            start_time = None

                    cv2.imshow(window_name, image)
                    key = cv2.waitKey(ESC_KEY) & 0xFF
                    if key == 27:
                        break
            else:
                # When we do not detect a line - this means we have probably gone off the lane or tilted
                # We should randomly turn back and forth as if we're looking for our lane again, assuming that
                # our rover simply tilted
                print("Passed")
                predicted_points = lane_tracker.predict(dt)
                if predicted_points is not None:
                    line_1 = ((predicted_points[0][0], predicted_points[0][1]),
                              (predicted_points[0][2], predicted_points[1][2]))
                    line_2 = ((predicted_points[1][0], predicted_points[1][1]),
                              (predicted_points[1][2], predicted_points[1][3]))

                    left_lane, right_lane = LaneDetector.get_left_right_lanes(line_1, line_2)
                    cv2.line(image, left_lane[0], left_lane[1], (255, 120, 80), 3)
                    cv2.line(image, right_lane[0], right_lane[1], (255, 120, 80), 3)
                    vp = line_intersection(left_lane, right_lane)
                    if vp is not None:
                        cv2.circle(image, tuple(vp), 10, (0, 244, 255), thickness=4)
                        dm_ds = warning_detection(height, width, image, vp, left_lane, right_lane)

                        movement = perceive_movement(dm_ds[0], dm_ds[1], width / 4)

                        if start_time is None:
                            start_time = datetime.now()
                            # client.handle_key(Keys.KEY_SPACE)
                            client.handle_key(movement)

                        elapsed_time = abs(datetime.now().second - start_time.second)
                        print("Elapsed Time in Else: ", elapsed_time)
                        if elapsed_time > 2:
                            start_time = None
                else:
                    # TODO: Randomly turn left and right
                    client.handle_key(Keys.KEY_SPACE)

                client.handle_key(Keys.KEY_SPACE)
                cv2.imshow(window_name, frame)
                key = cv2.waitKey(ESC_KEY) & 0xFF
                if key == 27:
                    break
                continue


def warning_detection(width, height, image, vp, left_lane, right_lane):
    """
    Returns the distance between the edges of the warning box and the points of intersection
    with the lanes.
    :param width: Image's width
    :param height: Image's height
    :param image: The actual image
    :param vp: The coordinate representing the vanishing point
    :param left_lane: The left lane
    :param right_lane: The right lane
    :return: tuple (dm, ds)
    """
    half_width = int(width / 2)
    half_height = int(height / 2)

    bottom_left = (vp[0] - half_width, vp[1] + half_height)
    bottom_right = (vp[0] + half_width, vp[1] + half_height)

    cv2.rectangle(image,
                  (vp[0] - half_width, vp[1]),
                  (vp[0] + half_width, vp[1] + half_height),
                  (0, 0, 255), thickness=2)

    warning_y = (int(vp[0] + half_width / 2), int(vp[1] + half_height))

    cv2.rectangle(image, (vp[0] - int(width / 4), vp[1]), warning_y, (244, 64, 130), thickness=2)

    m = line_intersection((bottom_left, bottom_right), left_lane)
    s = line_intersection((bottom_left, bottom_right), right_lane)
    if m is not None and s is not None:
        a_m = m[0]
        b_m = m[1]
        a_s = s[0]
        b_s = s[1]

        # Draw the left distance of the screen
        cv2.line(image, tuple(m), bottom_left, color=(66, 199, 244), thickness=4)
        # Draw the intersection
        cv2.circle(image, tuple(m), radius=4, color=(66, 199, 89), thickness=5)
        # Draw the right distance of the screen
        cv2.line(image, tuple(s), bottom_right, color=(66, 199, 244), thickness=4)
        # Draw the intersection
        cv2.circle(image, tuple(s), radius=4, color=(66, 199, 89), thickness=5)

        d_m = distance((a_m, b_m), bottom_left)
        d_s = distance((a_s, b_s), bottom_right)
        return d_m, d_s


def perceive_movement(d_m, d_s, threshold):
    """
    Checks the distance between the left and the right bounds. If d_m is larger than the threshold,
    force the rover to turn RIGHT. If d_s is larger than the threshold, force the rover to turn LEFT.
    The threshold is typically the image's width / 4.
    
    Steering should just return a state.
    
    :param d_m: distance from the left bound
    :param d_s: distance from the right bound
    :param threshold: Value determining if the car should steer or drive forward
    :return: None
    """
    if d_m > threshold:
        # print("Left")
        return common.Keys.KEY_LEFT
    elif d_s > threshold:
        # print("Right")
        return common.Keys.KEY_RIGHT
    else:
        # print("Straight")
        return common.Keys.KEY_UP

if __name__ == "__main__":
    main()
