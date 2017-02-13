import numpy as np
import cv2


class CameraError(Exception):
    pass


class Camera(object):
    def __init__(self, device=0):
        self.device = device
        self.camera = cv2.VideoCapture(self.device)

    def frame(self):
        status, frame = self.camera.read()
        if status:
            return frame
        else:
            raise CameraError("Cannot fetch frame")

    def close(self):
        if self.camera.isOpened():
            self.camera.release()

    def __del__(self):
        self.close()


if __name__ == '__main__':
    cam = Camera()
    cam.frame()
    cam.close()
