import numpy as np
import cv2
import pygame

from pygame.locals import *

class DataCollector(object):

    def __init__(self):

        self.FORW = 0
        self.BACK = 1
        self.RIGHT = 2
        self.LEFT = 3
        self.F_RIGHT = 4
        self.F_LEFT = 5


    def test_pygame(self):
        #Testing pygame
        pygame.init()
        pygame.display.set_mode()
        while True:
            for evt in pygame.event.get():
                if evt.type == KEYDOWN:
                    print("Help")
                    keyinput = pygame.key.get_pressed()
                    return


    def process_images(self, video):
        #TODO: change this to a stream computation

        frames = 0
        saved_frames = 0

        #for ML purposes, store images as numpy arrays
        #might want to convert to storing results of lane detection
        imglist = []
        labels = []
        pygame.init()
        screen = pygame.display.set_mode((640, 480))
        pygame.display.iconify()
        while video.isOpened():
            ret, frame = video.read()
            if not ret:
                break
            screen.fill([0,0,0])
            frames += 1
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = np.rot90(frame)
            frame = pygame.surfarray.make_surface(frame)
            screen.blit(frame, (0,0))
            pygame.display.update()
            pygame.time.wait(33) #30fps
            keyinput = pygame.key.get_pressed()

            if keyinput[pygame.K_UP]:
                print("Forward")
                labels.append(self.FORW)
            elif keyinput[pygame.K_RIGHT]:
                print("Right")
                labels.append(self.RIGHT)
            elif keyinput[pygame.K_LEFT]:
                print("Left")
                labels.append(self.LEFT)

            elif keyinput[pygame.K_DOWN]:
                print("Back")
                labels.append(self.BACK)
            else:
                labels.append(-1)

            for e in pygame.event.get():
                pass


        print(labels)
        print(len(labels))
        print(frames)
        #Number of labels and number of frames should be equal

if __name__ == '__main__':
    videopath = "./floor.mp4"
    x = DataCollector()
    cap = cv2.VideoCapture(videopath)
    x.process_images(cap)
