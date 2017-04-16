"""
http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html


Usage:
Here's a code snippet of how to use this API.
cam = Camera(image=False, video=True) # Instantiate our Camera class with video only
for i in range(0, 50):  # arbitary loop
    print(i)
    cam.frame()  # commit the frame to harddisk, also returns the frame
cam.close()  # properly close the camera


"""

from datetime import datetime
import os
from abc import ABCMeta, abstractmethod, abstractproperty
from image_processor import ImageProcessor, ESC_KEY

import numpy as np
import cv2


IMG_DIR = 'img/'
VIDEO_DIR = 'vid/'

FRAME_SIZE = (640, 480)


class CameraError(Exception):
    pass


class Writer(object):
    """
    The abstract base class that our video and image capture classes will use.
    Default behaviors are given as such:
    fps: 20
    size: 640px, 480px
    """
    __metaclass__ = ABCMeta

    def __init__(self, fps=20, size=FRAME_SIZE):
        if not isinstance(size, tuple):
            raise CameraError("Frame size parameter must be a tuple")

        self.size = size
        self.fps = fps
        self.frames_recorded = 0

    @abstractmethod
    def write(self, frame):
        pass

    @abstractmethod
    def close(self):
        pass

    def __repr__(self):
        return str(self.fps) + "fps" + " size: " + str(self.size)


class VideoWriter(Writer):
    """
    This class writers frames onto videos.
    """
    def __init__(self, output_name=None, *args, **kwargs):
        """
        Initialize our codec, DIVX, which is compatible on Windows (tested) and
        Linux.
        """
        super().__init__()
        timestamp = datetime.now().strftime('%m-%d-%y_%H-%M-%S')
        self.output_name = output_name or 'out_' + timestamp
        self.output_name = VIDEO_DIR + self.output_name + '.avi'
        print("out: " + self.output_name)
        codec = cv2.VideoWriter_fourcc(*'DIVX')
        self.writer = cv2.VideoWriter(self.output_name,
                                      codec,
                                      self.fps,
                                      self.size)

    def write(self, frame):
        self.writer.write(frame)
        # Make sure to increment frames_recorded
        self.frames_recorded += 1

    def __repr__(self):
        return str(self.writer)

    def close(self):
        self.writer.release()


class ImageWriter(Writer):
    """
    Writing image is simpler than videos. All you need is a frame and imwrite.
    """
    def write(self, frame, path=None):
        timestamp = datetime.now().strftime('%m-%d-%y_%H-%M-%S')
        cv2.imwrite((path or IMG_DIR) + str(self.frames_recorded) + '_' + timestamp + '.jpg', frame)
        # Make sure to increment frames_recorded
        self.frames_recorded += 1


    def close(self):
        """
        Nothing to dispose.
        """
        pass


class Camera(object):
    def __init__(self, device=0, video=False, image=False, video_writer=None,
                 image_writer=None):
        """
        Use video and image flags to control if video or image is written.

        device: int (device number) or str (video filename)
        video: bool
        image: bool
        video_writer: VideoWriter
        image_writer: ImageWriter
        """
        self.device = device
        self.camera = cv2.VideoCapture(self.device)

        # self.camera.set(cv2.CAP_PROP_FPS, 20)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

        if not self.camera.isOpened():
            raise CameraError('Failed to open camera!')

        self.write = video or image
        self.write_image = image
        self.write_video = video
        if self.write:
            self.check_dirs()
            if self.write_video:
                self.video_writer = video_writer or VideoWriter()
            if self.write_image:
                self.image_writer = image_writer or ImageWriter()
            print(self.video_writer)

    def check_dirs(self):
        if not os.path.exists(VIDEO_DIR):
            os.makedirs(VIDEO_DIR)

        if not os.path.exists(IMG_DIR):
            os.makedirs(IMG_DIR)

    def frame(self, delay_write=False):
        status, frame = self.camera.read()
        if status:
            if self.write and not delay_write:
                if self.write_video:
                    self._write_video_frame(frame)
                if self.write_image:
                    self.image_writer.write(frame)
            return frame
        else:
            raise CameraError("Cannot fetch frame")

    def _write_video_frame(self, frame):
        self.video_writer.write(frame)

    def preprocess(self, frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    def close(self):
        """
        Properly dispose of resources.
        """
        if self.camera.isOpened():
            self.camera.release()
        if self.write_video:
            self.video_writer.close()
        if self.write_image:
            self.image_writer.close()

    def __del__(self):
        self.close()


class VideoReader(object):
    """
    Reads a video frame by frame and processes each frame
    """
    def __init__(self, video_path):
        self.video_path = video_path
        self.video = None

    def open_video(self):
        self.video = cv2.VideoCapture(self.video_path)
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_SIZE[0])
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_SIZE[1])
        return self.video

    def read_video(self):
        while self.video.isOpened():
            ret, frame = self.video.read()
            yield frame, self.video.isOpened()

if __name__ == '__main__':
    cam = Camera(image=True, video=True)
    for i in range(0, 50):
        cv2.imshow("f", cam.frame())
    cam.close()
