from PIL import Image, ImageTk
import os

from constants import IMAGE_DIRECTORY, STRONG, NORMAL, BARRIER, BACKGROUND_FILENAME


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
        if brick_type == STRONG:
            brick_type = NORMAL
        brick_color = brick.get_color()
        image_key = f'brick-{brick_color}-{brick_type}.png'
        return self.images[image_key]

    def get_background(self):
        return self.images[BACKGROUND_FILENAME]
