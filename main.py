import time
import os
from image_processor import FileManager, ImageProcessor, ESC_KEY
from camera import IMG_DIR, VIDEO_DIR, VideoReader, FRAME_SIZE
from calibration import calibrate_canny
import cv2
from lane_tracking.detect import LaneDetector
from lane_tracking import ransac_vanishing_point

try:
    from rover import RoverClient

    rover = RoverClient()
    rover_status = True
except:
    rover_status = False

LIVE_STREAM = "http://192.168.1.107:8080/?action=stream"


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


def get_intersection(line_1:tuple, line_2: tuple) -> tuple:
    """
    Finds the intersection of two lines
    :param line_1: A pair of (x,y) coordinates defining a line
    :param line_2: A pair of (x`, y`) coordinates defining a line
    :return: Coordinate defining the intersection
    """
    def get_slope(line:tuple) -> float:
        p1 = line[0]
        p2 = line[1]
        return (p1[1] - p2[1]) / (p1[0] - p2[0])

    def get_y_intersect(slope: float, point: tuple) -> float:
        """
        Gets the y intersect of a line
        :param slope: slope of the line
        :param point: (x, y) coordinate
        :return: b, the y intercept
        """
        pass
    pass


def main():
    image_processor = ImageProcessor()
    if os.environ.get("VIDEO_PATH") is not None:
        video = VideoReader(0)
    else:
        # video = VideoReader(LIVE_STREAM)
        video = VideoReader("{}{}".format(VIDEO_DIR, "hough_transform_sample.mp4"))
    cap = video.open_video()

    lane_detect = LaneDetector(50)
    while cap.isOpened():
        ret, frame = cap.read()

        height = frame.shape[0]
        width = frame.shape[1]

        image = frame # Cache the frame being rendered
        image = image_processor.bilateral_blur(image) # Maybe execute this on a different thread - pretty slow right now
        points = lane_detect.detect(image)
        image_processor.find_points(width, height)

        if points is not None:
            if points[0] is not None and points[1] is not None:
                l_p1 = (int(points[0][0]), points[0][1])
                l_p2 = (int(points[0][2]), points[0][3])
                r_p1 = (int(points[1][0]), points[1][1])
                r_p2 = (int(points[1][2]), points[1][3])

                cv2.line(image, l_p1, l_p2, (0, 255, 0), 2)
                cv2.line(image, r_p1, r_p2, (0, 255, 0), 2)

                intersection = line_intersection((l_p1, l_p2), (r_p1, r_p2))

                if intersection is not None:
                    cv2.circle(image, tuple(intersection), 1, (0, 255, 0), thickness=2)

            else:
                # print(points)
                continue

        image = image_processor.draw_horizontal_line(image)
        image = image_processor.draw_midpoint_line(image)

        cv2.imshow("", image)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            cap.close()
            break


def image_process():
    file_manager = FileManager()
    # Hard coded the threshold values for the images
    image_processor = ImageProcessor(threshold_1=114, threshold_2=237)
    images = file_manager.get_image_files(IMG_DIR)

    for image_path in images:
        image = cv2.imread(image_path)
        blurred_image = image_processor.bilateral_blur(image)
        cv2.imshow("Original", image)
        cv2.imshow("Blurred", blurred_image)

        while True:
            if cv2.waitKey(1) & 0XFF == ord("q"):
                break


def video_process():
    image_processor = ImageProcessor(threshold_1=1000, threshold_2=2000)
    image_processor.aperture_size = 5
    # video = VideoReader("{}{}".format(VIDEO_DIR, "hough_transform_sample.mp4"))
    if os.environ.get('VIDEO_PATH') is not None:
        video = VideoReader(0)
    else:
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
            continue

        image_processor.find_points(width, height)

        image = image_processor.draw_horizontal_line(image)
        image = image_processor.draw_midpoint_line(image)

        # hough_transformed_image = image_processor.phough_transform(edged_image, frame)

        # cv2.imshow("Edged", edged_image)
        # cv2.imshow("Hough Transform", hough_transformed_image)
        try:
            best_fit = ransac_vanishing_point.ransac_vanishing_point_detection(
                [[points[0][0], points[0][1], points[0][2], points[0][3]],
                 [points[1][0], points[1][1], points[1][2], points[1][3]]])
        except ZeroDivisionError:
            continue
        if best_fit:
            cv2.circle(frame, best_fit, 10, (0, 244, 255), thickness=5)

            # warning box
            height = frame.shape[0]
            width = frame.shape[1]

            cv2.rectangle(frame, (best_fit[0] - int(width / 2), best_fit[1]),
                          (best_fit[0] + int(width / 2), best_fit[1] + int(height / 2)), (0, 244, 255), thickness=2)
            bottom_left = (best_fit[0] - int(width / 2), best_fit[1] + int(height / 2))
            bottom_right = (best_fit[0] + int(width / 2), best_fit[1] + int(height / 2))
            M = line_intersection((bottom_left, bottom_right),
                                  ([points[0][0], points[0][1]], [points[0][2], points[0][3]]))
            S = line_intersection((bottom_left, bottom_right),
                                  ([points[1][0], points[1][1]], [points[1][2], points[1][3]]))

            # if M is not None and M[0] >= bottom_left[0] and S is not None and S[0] <= bottom_right[0]:
            if M is not None and S is not None:
                # dM[0] -= predicted[0][0]
                # Draw the left side of the screen
                cv2.line(frame, tuple(M), bottom_left, (66, 244, 89), thickness=5)
                cv2.circle(frame, tuple(M), radius=5, color=(66, 244, 89), thickness=5)
                # Draw the right side of the screen
                cv2.line(frame, tuple(S), bottom_right, (66, 244, 89), thickness=5)
                cv2.circle(frame, tuple(S), radius=5, color=(66, 244, 89), thickness=5)

                if M[0] > 0 and not None:
                    d_M = (((best_fit[1] + height / 2) - M[1]) / M[0]) - (best_fit[0] - width / 2)
                    d_S = (best_fit[0] + width / 2) - (((best_fit[1] + height / 2) - S[1]) / S[0])
                else:
                    d_M = (best_fit[0] + width / 2) - (((best_fit[1] + height / 2) - M[1]) / M[0])
                    d_S = (((best_fit[1] + height / 2) - S[1]) / S[0]) - (best_fit[0] - width / 2)

                if d_M > width:
                    # print("DM: {}, DS: {}, Image Width: {}".format(d_M, d_S, width / 4))
                    cv2.putText(frame, "Right: DM: {}, DS: {}, Frame Width: {}".format(d_M, d_S, width),
                                (0, 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
                    print("Right")
                    if rover_status:
                        rover.forward_right()
                elif d_S > width:
                    cv2.putText(frame, "Left: DM: {}, DS: {}, Frame Width: {}".format(d_M, d_S, width),
                                (0, 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
                    print("Left")
                    if rover_status:
                        rover.forward_left()
                else:
                    cv2.putText(frame, "Straight: DM: {}, DS: {}, Frame Width: {}".format(d_M, d_S, width),
                                (0, 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
                    print("Straight")
                    if rover_status:
                        rover.forward()
            else:
                cv2.putText(frame, "Straight", (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
                print("Straight")
                if rover_status:
                    rover.forward()

            warning_y = (best_fit[0] + int(width / 4), best_fit[1] + int(height / 2))
            # danger box
            # offset = int(frame.shape[0] / 2 / 2)
            # offset = int(frame.shape[1]/4)
            cv2.rectangle(frame, (best_fit[0] - int(width / 4), best_fit[1]),
                          warning_y, (244, 65, 130),
                          thickness=2)
            time.sleep(.5)

        try:
            cv2.imshow("", image)
            key = cv2.waitKey(ESC_KEY)

            if ESC_KEY == 27:
                break
        except:
            # Doesn't support imshow
            pass

if __name__ == "__main__":
    main()
    # video_process()
    # calibrate_canny("{}{}".format(VIDEO_DIR, "home_grown.webm"))
    # image_process()
