import socket
import os
import cv2

from .common import UDP_IP_PORT, UDP_IP, UDP_PORT
import camera


print("Connecting client on UDP {0}:{1}".format(UDP_IP, UDP_PORT))
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def capture_keys():
    k = cv2.waitKey(0)
    if k == 2490368:  # up
        sock.sendto(b"up", UDP_IP_PORT)
    elif k == 2621440:  # down
        sock.sendto(b"down", UDP_IP_PORT)
    elif k == 2424832:  # left
        sock.sendto(b"left", UDP_IP_PORT)
    elif k == 2555904:  # right
        sock.sendto(b"right", UDP_IP_PORT)
    elif k == 32:
        sock.sendto(b"space", UDP_IP_PORT)


if __name__ == '__main__':
    cap = camera.Camera()

    while cap.camera.isOpened():
        cv2.imshow("stream", cap.frame())
        capture_keys()
