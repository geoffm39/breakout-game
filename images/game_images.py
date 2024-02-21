from PIL import Image, ImageTk
import os

from brick import Brick
from constants import (
    IMAGE_DIRECTORY, STRONG, NORMAL, BACKGROUND_FILENAME, POWERUP_FILENAME, PADDLE_FILENAME,
    PADDLE_WIDTH
)


class GameImages:
    def __init__(self):
        self.images = {}
        self.paddle_image = None

        self.load_images()

    def load_images(self):
        for filename in os.listdir(IMAGE_DIRECTORY):
            image_path = os.path.join(IMAGE_DIRECTORY, filename)
            with Image.open(image_path) as image:
                photo_image = ImageTk.PhotoImage(image)
            self.images[filename] = photo_image

    def get_brick_image(self, brick: Brick):
        brick_type = brick.get_type()
        if brick_type == STRONG:
            brick_type = NORMAL
        brick_color = brick.get_color()
        image_key = f'brick-{brick_color}-{brick_type}.png'
        return self.images[image_key]

    def get_background(self):
        return self.images[BACKGROUND_FILENAME]

    def get_paddle(self):
        image_path = os.path.join(IMAGE_DIRECTORY, PADDLE_FILENAME)
        with Image.open(image_path) as image:
            self.paddle_image = image.copy()
        return self.images[PADDLE_FILENAME]

    def get_resized_paddle(self, paddle_length):
        paddle_pixel_length = paddle_length * PADDLE_WIDTH
        resized_image = self.paddle_image.copy()
        resized_image = resized_image.resize((paddle_pixel_length, PADDLE_WIDTH))
        self.images[PADDLE_FILENAME] = ImageTk.PhotoImage(resized_image)
        return self.images[PADDLE_FILENAME]

    def get_powerup(self):
        return self.images[POWERUP_FILENAME]
