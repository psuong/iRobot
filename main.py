from image_processor import FileManager, ImageProcessor
from camera import IMG_DIR, VIDEO_DIR, VideoReader


def main():
    file_manager = FileManager()
    image_processor = ImageProcessor()

    image_files = file_manager.get_image_files(IMG_DIR)
    for image in image_files:
        edged_image = image_processor.edge_detect(image)
        image_processor.phough_transform(edged_image)


def video_process():
    video = VideoReader("{}{}".format(VIDEO_DIR, "hough_transform_sample.mp4"))
    image_processor = ImageProcessor()

    video.__image_processor__ = image_processor
    video.open_video()
    video.read_video()


if __name__ == "__main__":
    # main()
    video_process()

