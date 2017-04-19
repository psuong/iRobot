from __future__ import division

import cv2

from lane_tracking import track, detect, ransac_vanishing_point
from time import  sleep
from rover import RoverClient
from camera import Camera


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
    return [x, y]


def main(video_path, show_window=True):
    rover = RoverClient()
    cap = Camera(device=video_path, video=True)
    rover.forward()
    # Wait and sleep
    sleep(1)
    ticks = 0

    lt = track.LaneTracker(2, 0.1, 500)
    ld = detect.LaneDetector(80)
    while True:
        precTick = ticks
        ticks = cv2.getTickCount()
        dt = (ticks - precTick) / cv2.getTickFrequency()

        frame = cap.frame(delay_write=True)

        predicted = lt.predict(dt)

        lanes = ld.detect(frame)

        if predicted is not None:
            cv2.line(frame, (predicted[0][0], predicted[0][1]), (predicted[0][2], predicted[0][3]), (255, 0, 255), 2)
            cv2.line(frame, (predicted[1][0], predicted[1][1]), (predicted[1][2], predicted[1][3]), (255, 0, 255), 2)

            best_fit = ransac_vanishing_point.ransac_vanishing_point_detection(
                [[predicted[0][0], predicted[0][1], predicted[0][2], predicted[0][3]],
                 [predicted[1][0], predicted[1][1], predicted[1][2], predicted[1][3]]])
            if best_fit:
                cv2.circle(frame, best_fit, 10, (0, 244, 255), thickness=5)

                # warning box
                height = frame.shape[0]
                width = frame.shape[1]

                cv2.rectangle(frame, (best_fit[0] - int(width/2), best_fit[1]), (best_fit[0] + int(width/2), best_fit[1] + int(height/2)), (0, 244, 255), thickness=2)
                bottom_left = (best_fit[0] - int(width / 2), best_fit[1] + int(height / 2))
                bottom_right = (best_fit[0] + int(width / 2), best_fit[1] + int(height / 2))
                M = line_intersection((bottom_left, bottom_right),
                                      ([predicted[0][0], predicted[0][1]], [predicted[0][2], predicted[0][3]]))
                S = line_intersection((bottom_left, bottom_right),
                                       ([predicted[1][0], predicted[1][1]], [predicted[1][2], predicted[1][3]]))

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
                        rover.forward_right()
                    elif d_S > width:
                        cv2.putText(frame, "Left: DM: {}, DS: {}, Frame Width: {}".format(d_M, d_S, width),
                                    (0, 20),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
                        print("Left")
                        rover.forward_left()
                    else:
                        cv2.putText(frame, "Straight: DM: {}, DS: {}, Frame Width: {}".format(d_M, d_S, width),
                                    (0, 20),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
                        print("Straight")
                        rover.forward()
                else:
                    cv2.putText(frame, "Straight", (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
                    print("Straight")
                    rover.forward()

                warning_y = (best_fit[0] + int(width / 4), best_fit[1] + int(height / 2))
                # danger box
                # offset = int(frame.shape[0] / 2 / 2)
                # offset = int(frame.shape[1]/4)
                cv2.rectangle(frame, (best_fit[0] - int(width / 4), best_fit[1]),
                              warning_y, (244, 65, 130),
                              thickness=2)
                cap._write_video_frame(frame)
                sleep(1)
        lt.update(lanes)
        
        if show_window:
            cv2.imshow('', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.close()
            break


if __name__ == '__main__':
    # main('E:/Users/exp0nge/projects/iRobot/vid/straight.webm')
    # main('E:/Users/exp0nge/projects/iRobot/vid/curved.mp4')
    # main("vids/straight-2.mp4")
    # main("vids/hough_transform_sample.mp4")
    # main("vids/curved_roads.mp4")
    main(0, show_window=False)