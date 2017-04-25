import numpy as np
import cv2
import pygame

from pygame.locals import *

class DataCollector(object):

    def __init__(self):

        pygame.init()
        self.FORW = 0
        self.BACK = 1
        self.RIGHT = 2
        self.LEFT = 3
        self.F_RIGHT = 4
        self.F_LEFT = 5



    def process_images(self, video):
        #TODO: change this to a stream computation
        #unless we want


        while video.isOpened():
            ret, frame = video.read()
            cv2.imshow('', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break





if __name__ == '__main__':
    videopath = "./floor.mp4"
    x = DataCollector()
    cap = cv2.VideoCapture(videopath)
    x.process_images(cap)
