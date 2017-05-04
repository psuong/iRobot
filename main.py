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


def video_process():
    if os.environ.get('VIDEO_PATH') is not None:
        camera_stream = WebcamVideoStream(src=0).start()
    else:
        camera_stream = WebcamVideoStream(src=1).start()
        # camera_stream = WebcamVideoStream(src="{}{}".format(VIDEO_DIR, "/hough_transform_sample.mp4"))

    thread_manager = ThreadManager()
    lane_detect = LaneDetector(50)

    while camera_stream.stream.isOpened():
        frame = camera_stream.read()

        if frame is not None:
            height = frame.shape[0]
            width = frame.shape[1]

            # thread_manager.start_single_thread(funct=image_processor.bilateral_blur, args=(frame, thread_manager.queue))
            # image = thread_manager.peek()
            # image = ImageProcessor.filter_colors(frame)
            image = cv2.blur(frame, (10, 10))
            points = lane_detect.detect(image)

            if points is not None:
                if points[0] is not None and points[1] is not None:
                    l_p1 = (int(points[0][0]), points[0][1])
                    l_p2 = (int(points[0][2]), points[0][3])
                    r_p1 = (int(points[1][0]), points[1][1])
                    r_p2 = (int(points[1][2]), points[1][3])

                    image_processor.update_lanes((l_p1[0], l_p1[1], l_p2[0], l_p2[1]), (r_p1[0], r_p1[1], r_p2[0], r_p2[1]))

                    cv2.line(image, l_p1, l_p2, (0, 255, 0), 2)
                    cv2.line(image, r_p1, r_p2, (0, 255, 0), 2)
            else:
                print(points)
                continue

            image_processor.find_points(width, height)

            image = image_processor.draw_horizontal_line(image)
            image = image_processor.draw_midpoint_line(image)

            try:
                if points[0] is not None and points[1] is not None:
                    line_1 = ((points[0][0], points[0][1]), (points[0][2], points[0][3]))
                    line_2 = ((points[1][0], points[1][1]), (points[1][2], points[1][3]))

                    vp = line_intersection(line_1, line_2)

                    if vp:
                        cv2.circle(image, tuple(vp), 10, (0, 244, 255), thickness=5)

                        # warning box
                        height = frame.shape[0]
                        width = frame.shape[1]

                        # Draw the warning box
                        cv2.rectangle(image, (vp[0] - int(width / 2), vp[1]),
                                      (vp[0] + int(width / 2), vp[1] + int(height / 2)), (0, 0, 255), thickness=2)

                        # Store the bottom left and right
                        bottom_left = (vp[0] - int(width / 2), vp[1] + int(height / 2))
                        bottom_right = (vp[0] + int(width / 2), vp[1] + int(height / 2))

                        # Calculate the coordinates for the left and right hand intersections
                        M = line_intersection((bottom_left, bottom_right),
                                              ([points[0][0], points[0][1]], [points[0][2], points[0][3]]))
                        S = line_intersection((bottom_left, bottom_right),
                                              ([points[1][0], points[1][1]], [points[1][2], points[1][3]]))

                        if M is not None and S is not None:
                            # Cache the left hand coordinates and right hand coordinates
                            a_m = M[0]
                            b_m = M[1]
                            a_s = S[0]
                            b_s = S[1]

                            # Draw the left side of the screen
                            cv2.line(image, tuple(M), bottom_left, (66, 244, 89), thickness=5)
                            # Draw the intersection between the bottom left hand corner and the lane
                            cv2.circle(image, tuple(M), radius=5, color=(66, 244, 89), thickness=5)
                            # Draw the right side of the screen
                            cv2.line(image, tuple(S), bottom_right, (66, 244, 89), thickness=5)
                            # Draw the intersection between the bottom right hand corner and the lane
                            cv2.circle(image, tuple(S), radius=5, color=(66, 244, 89), thickness=5)

                            # Calculate the distance between the left and right hand intersections and edges
                            # of the warning box
                            d_M = math.sqrt(math.pow((bottom_left[0] - a_m), 2) + math.pow((bottom_left[1] - b_m), 2))
                            d_S = math.sqrt(math.pow((bottom_right[0] - a_s), 2) + math.pow((bottom_right[1] - b_s), 2))

                            # If the distance between the left and right hand side is too large then we tell the rover
                            # to turn left or right
                            if d_M > width / 4:
                                # Turns the rover left
                                cv2.putText(frame, "Left: DM: {}, DS: {}, Frame Width: {}".format(d_M, d_S, width),
                                            (0, 20),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255))
                                print("LEFT")
                                if rover_status:
                                    rover.forward_left()
                            elif d_S > height / 4:
                                # Turns the rover right
                                cv2.putText(frame, "Right: DM: {}, DS: {}, Frame Width: {}".format(d_M, d_S, width),
                                            (0, 20),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255))
                                print("RIGHT")
                                if rover_status:
                                    rover.forward_right()
                            else:
                                cv2.putText(frame, "Straight: DM: {}, DS: {}, Frame Width: {}".format(d_M, d_S, width),
                                            (0, 20),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255))
                                print("STRAIGHT")
                                if rover_status:
                                    rover.forward()
                        else:
                            cv2.putText(frame, "Straight", (0, 20),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255))
                            print("STRAIGHT")
                            client.handle_key(Keys.KEY_UP)
                            if rover_status:
                                rover.forward()

                        warning_y = (vp[0] + int(width / 4), vp[1] + int(height / 2))
                        # danger box
                        # offset = int(frame.shape[0] / 2 / 2)
                        # offset = int(frame.shape[1]/4)
                        cv2.rectangle(frame, (vp[0] - int(width / 4), vp[1]),
                                      warning_y, (244, 65, 130),
                                      thickness=2)
                    try:
                        cv2.imshow("", image)
                        key = cv2.waitKey(ESC_KEY) & 0XFF

                        if key == 27:
                            break
                    except:
                        # Doesn't support imshow
                        pass
            except ZeroDivisionError:
                pass
        else:
            camera_stream.stream.release()


def preview():
    camera_stream = WebcamVideoStream(src=1).start()

    while camera_stream.stream.isOpened():
        frame = camera_stream.read()

        cv2.imshow("", frame)
        cv2.waitKey(1) & 0xFF


if __name__ == "__main__":
    video_process()
    # preview()