from image_processor import FileManager, ImageProcessor, ESC_KEY
from camera import IMG_DIR, VIDEO_DIR, VideoReader
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
    image_processor = ImageProcessor()
    video = VideoReader("{}{}".format(VIDEO_DIR, "home_grown.webm"))

    capture = video.open_video()

    while capture.isOpened():
        ret, frame = capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edged_image = image_processor.edge_detect(gray)
        hough_transformed_image = image_processor.phough_transform(edged_image, frame)

        cv2.imshow("Window", hough_transformed_image)
        cv2.imshow("Edged", edged_image)

        key = cv2.waitKey(ESC_KEY)

        if ESC_KEY == 27:
            break

    video_generator = video.read_video()

    for image, status in video_generator:
        if status:
            ret, frame = video.video.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            edged_image = image_processor.edge_detect(gray)
            hough_transformed_image = image_processor.phough_transform(edged_image, frame)
            cv2.imshow("Window", hough_transformed_image)


if __name__ == "__main__":
    # main()
    video_process()
    # calibrate_canny("{}{}".format(VIDEO_DIR, "home_grown.webm"))
