from image_processor import FileManager, ImageProcessor
from camera import IMG_DIR, VIDEO_DIR


def main():
    file_manager = FileManager()
    image_processor = ImageProcessor()

    image_files = file_manager.get_image_files(IMG_DIR)
    for image in image_files:
        edged_image = image_processor.edge_detect(image)
        image_processor.phough_transform(edged_image)


if __name__ == "__main__":
    main()

