import os
import cv2

from image_processor import ImageProcessor
from camera import ImageWriter, VideoReader


class CannyVideoProcessor(ImageProcessor):
    def __init__(self, video_path, threshold_1, threshold_2, *args, **kwargs):
        super().__init__(threshold_1=threshold_1, threshold_2=threshold_2)
        self.video_reader = VideoReader(video_path)
        self.image_writer = ImageWriter()

    def stream(self):
        img, status = self.video_reader.read_video()
        canny_image = super().edge_detect(img)
        self.image_writer.write(canny_image, path='samples/images/')
        if status:
            stream()


if __name__ == '__main__':
    threshold_1 = 733
    threshold_2 = 205
    image_processor = ImageProcessor(show_image=True, threshold_1=threshold_1, threshold_2=threshold_2)
    image_processor.edge_detect(cv2.imread('samples/images/1_bed.jpg'))
