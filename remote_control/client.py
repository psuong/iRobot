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
    print("sending ", k, " to ", UDP_IP_PORT)
    if k == 2490368 or k == Keys.KEY_UP:  # up
        sock.sendto(Keys.KEY_UP.value, UDP_IP_PORT)
    elif k == 2621440 or k == Keys.KEY_DOWN:  # down
        sock.sendto(Keys.KEY_DOWN.value, UDP_IP_PORT)
    elif k == 2424832 or k == Keys.KEY_LEFT:  # left
        sock.sendto(Keys.KEY_LEFT.value, UDP_IP_PORT)
    elif k == 2555904 or k == Keys.KEY_RIGHT:  # right
        sock.sendto(Keys.KEY_RIGHT.value, UDP_IP_PORT)
    elif k == 32 or k == Keys.KEY_SPACE:
        sock.sendto(Keys.KEY_SPACE.value, UDP_IP_PORT)
    else:
        print("can't process", k)


if __name__ == '__main__':
    sock.sendto(b"hello", UDP_IP_PORT)
