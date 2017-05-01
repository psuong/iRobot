from datetime import datetime
from threading import Thread
import cv2


class FrameCounter(object):
    def __init__(self):
        self.start = None
        self.end = None
        self.num_of_frames = 0

    def start(self):
        self.start = datetime.now()
        return self

    def end(self):
        self.end = datetime.now()
        return self

    def update_frames(self):
        self.num_of_frames += 1

    def find_elapsed_time(self):
        return (self.end - self.start).total_seconds()

    def get_fps(self):
        return self.num_of_frames / self.find_elapsed_time()


class WebCamThread(object):
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        (self.ret, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        Thread(target=self.update(), args=()).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return

            (self.ret, self.frame) = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True
