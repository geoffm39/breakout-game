from PIL import Image, ImageTk
import os

from constants import IMAGE_DIRECTORY


class GameImages:
    def __init__(self):
        self.images = {}

        self.load_images()

    def load_images(self):
        for filename in os.listdir(IMAGE_DIRECTORY):
            image_path = os.path.join(IMAGE_DIRECTORY, filename)
            with Image.open(image_path) as image:
                photo_image = ImageTk.PhotoImage(image)
            self.images[filename] = photo_image

    def get_brick_image(self, brick):
        brick_type = brick.get_type()
        brick_color = brick.get_color()
        image_key = f'brick-{brick_color}-{brick_type}.png'
