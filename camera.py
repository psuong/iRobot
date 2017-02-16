"""
http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
"""

from datetime import datetime
import os

import numpy as np
import cv2


IMG_DIR = 'img/'
VIDEO_DIR = 'vid/'


class CameraError(Exception):
    pass


class CameraWriter(object):
    def __init__(self, output_name=None, fps=20, size=(640, 480), write_img=False):
        timestamp = datetime.now().strftime('%m-%d-%y_%H-%M-%S')
        self.output_name = output_name or "out_" + timestamp
        self.output_name = VIDEO_DIR + self.output_name + '.avi'
        self.fps = fps
        if not isinstance(size, tuple):
            raise Camera("Frame size parameter must be a tuple")
        self.size = size

        codec = cv2.VideoWriter_fourcc(*'DIVX')
        self.writer = cv2.VideoWriter(output_name, codec, fps, size)

        self.write_img = write_img
        self.frames_recorded = 0

    def write(self, frame):
        self.writer.write(frame)

        if self.write_img:
            self.__write_img(frame)

        self.frames_recorded += 1

    def __write_img(self, frame):
        timestamp = datetime.now().strftime('%m-%d-%y_%H-%M-%S')
        cv2.imwrite(IMG_DIR + timestamp + '.jpg', frame)

    def close(self):
        self.writer.release()

    def __repr__(self):
        return self.output_name + " @ " + str(self.fps) + "fps" + " size: " + str(self.size)


class Camera(object):
    def __init__(self, device=0, video=False, image=False, writer=None):
        self.device = device
        self.camera = cv2.VideoCapture(self.device)
        self.write = video or image
        if self.write:
            self.check_dirs()

            self.writer = writer or CameraWriter(write_img=image)
            print(str(self.writer))

    def check_dirs(self):
        if not os.path.exists(VIDEO_DIR):
            os.makedirs(VIDEO_DIR)

        if not os.path.exists(IMG_DIR):
            os.makedirs(IMG_DIR)

    def frame(self):
        status, frame = self.camera.read()
        if status:
            frame = self.preprocess(frame)
            if self.write:
                self.writer.write(cv2.flip(frame, 0))
            return frame
        else:
            raise CameraError("Cannot fetch frame")


    def preprocess(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    def close(self):
        if self.camera.isOpened():
            self.camera.release()
        if self.write:
            self.writer.close()

    def __del__(self):
        self.close()



if __name__ == '__main__':
    cam = Camera(image=True)
    for i in range(0, 30):
        print(i)
        cam.frame()
    cam.close()
