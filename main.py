from image_processor import FileManager, ImageProcessor
from camera import IMG_DIR, VIDEO_DIR, VideoReader


def main():
    file_manager = FileManager()
    image_processor = ImageProcessor()
    pass


def video_process():
    image_processor = ImageProcessor()
    video = VideoReader("{}{}".format(VIDEO_DIR, "hough_transform_sample.mp4"), image_processor)

    video.open_video()
    video.read_video()


if __name__ == "__main__":
    # main()
    video_process()

