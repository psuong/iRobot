from image_processor import FileManager, ImageProcessor, ESC_KEY
from camera import IMG_DIR, VIDEO_DIR, VideoReader, FRAME_SIZE
from calibration import calibrate_canny
import cv2


def main():
    file_manager = FileManager()
    image_processor = ImageProcessor()


def image_process():
    file_manager = FileManager()
    # Hard coded the threshold values for the images
    image_processor = ImageProcessor(threshold_1=114, threshold_2=237)

    file_manager.get_image_files(IMG_DIR)


def video_process():
    image_processor = ImageProcessor(threshold_1=1000, threshold_2=2000)
    image_processor.aperture_size = 5
    video = VideoReader("{}{}".format(VIDEO_DIR, "curved_roads.mp4"))

    capture = video.open_video()

    while capture.isOpened():
        ret, frame = capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edged_image = image_processor.edge_detect(gray)
        hough_transformed_image = image_processor.phough_transform(edged_image, frame)

        cv2.imshow("Edged", edged_image)
        cv2.imshow("Hough Transform", hough_transformed_image)

        key = cv2.waitKey(ESC_KEY)

        if ESC_KEY == 27:
            break


if __name__ == "__main__":
    # main()
    video_process()
    # calibrate_canny("{}{}".format(VIDEO_DIR, "home_grown.webm"))
