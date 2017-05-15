import numpy as np
import pygame
import os
import cv2
import math
import random
from image_processor import ImageProcessor, ESC_KEY
from lane_tracking.detect import LaneDetector
from imutils.video import WebcamVideoStream
from remote_control import client
from remote_control.common import MotorManager
from remote_control.client import Keys
from calibration_data import HSVData, UPPER_BOUND, LOWER_BOUND, DATA_DIR, load_serialize_data
from utility import line_intersection, distance, get_average_line
from lane_tracking.track import LaneTracker
from datetime import datetime

from remote_control import client, common


try:
    from rover import RoverClient

    rover = RoverClient()
    rover_status = True
except:
    rover_status = False

LIVE_STREAM = "http://192.168.43.164:8080/?action=stream"
image_processor = ImageProcessor(threshold_1=1000, threshold_2=2000)

from pygame.locals import *

class DataCollector(object):
    if os.environ.get('VIDEO_PATH') is None:
        camera_stream = WebcamVideoStream(src=LIVE_STREAM).start()
    else:
        camera_stream = WebcamVideoStream(src=1).start()

    motor_manager = MotorManager(0.5)

    def __init__(self):

        self.FORW = 0
        self.BACK = 1
        self.RIGHT = 2
        self.LEFT = 3
        self.F_RIGHT = 4
        self.F_LEFT = 5

    def process_images(self, video):
        #TODO: change this to a stream computation
        #right now it works on prerecorded videos

        frames = 0
        saved_frames = 0

        #307200 pixels in each image
        #probably need to downscale, training is slow
        framearray = np.zeros((1, 38400)).astype(np.float32)
        labelarray = np.zeros((1,4)).astype(np.float32)

        #for ML purposes, store images as numpy arrays
        #might want to convert to storing results of lane detection
        imglist = []
        labels = []
        pygame.init()
        screen = pygame.display.set_mode((320, 240))

    while camera_stream.stream.isOpened():
            frame = camera_stream.read()
            if not ret:
                break

            #keep count of frames
            frames += 1

            #draw to screen using pygame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = gray.reshape(1, 38400).astype(np.float32)
            screen.fill([0,0,0])
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            frame = pygame.surfarray.make_surface(frame)
            screen.blit(frame, (0,0))
            pygame.display.update()
            pygame.time.wait(1) #30fps


            labelrow = [0,0,0,0]
            #get keypresses
            keyinput = pygame.key.get_pressed()
            if keyinput[pygame.K_UP]:
                print("Forward")
                labelrow[self.FORW] = 1
            elif keyinput[pygame.K_RIGHT]:
                print("Right")
                labelrow[self.RIGHT]= 1
            elif keyinput[pygame.K_LEFT]:
                print("Left")
                labelrow[self.LEFT]= 1
            elif keyinput[pygame.K_DOWN]:
                print("Back")
                labelrow[self.BACK] = 1
            else:
                labels.append(-1)

            #pygame event queue must be refreshed
            for e in pygame.event.get():
                pass

            print(framearray.shape)
            print(gray.shape)
            framearray = np.vstack((framearray, gray))

            print(labelrow)

            #TODO: modify this for more directions
            #than 4

            labelarray = np.vstack((labelarray, np.asarray(labelrow).astype(np.float32)))

        #labels now has a label for each videoframe
        print(labelarray)
        print(len(labels))
        print(frames)



        np.save("videolabels", labelarray)
        np.save("framedata", framearray)



if __name__ == '__main__':
    videopath = "./floor.mp4"
    x = DataCollector()
    cap = cv2.VideoCapture(videopath)
    x.process_images(cap)
