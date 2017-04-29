import socket
import cv2

from .common import UDP_IP_PORT, UDP_IP, UDP_PORT, Keys
import camera

print("Connecting client on UDP {0}:{1}".format(UDP_IP, UDP_PORT))
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def capture_keys():
    k = cv2.waitKey(0)
    handle_key(k)


def handle_key(k):
    if k == 2490368:  # up
        sock.sendto(Keys.KEY_UP.value, UDP_IP_PORT)
    elif k == 2621440:  # down
        sock.sendto(Keys.KEY_DOWN.value, UDP_IP_PORT)
    elif k == 2424832:  # left
        sock.sendto(Keys.KEY_LEFT.value, UDP_IP_PORT)
    elif k == 2555904:  # right
        sock.sendto(Keys.KEY_RIGHT.value, UDP_IP_PORT)
    elif k == 32:
        sock.sendto(Keys.KEY_SPACE.value, UDP_IP_PORT)


if __name__ == '__main__':
    sock.sendto("hello", UDP_IP_PORT)
