from PIL import Image, ImageTk
import os

from brick import Brick
from paddle import Paddle
from constants import (
    IMAGE_DIRECTORY, STRONG, NORMAL, BACKGROUND_FILENAME, POWERUP_FILENAME, PADDLE_FILENAME,
    PADDLE_WIDTH, PADDLE_LASERS_FILENAME, LASER_FILENAME
)


class GameImages:
    def __init__(self):
        self.photo_images = {}
        self.paddle_image = None
        self.laser_paddle_image = None

        self.load_images()

    def load_images(self):
        for filename in os.listdir(IMAGE_DIRECTORY):
            image_path = os.path.join(IMAGE_DIRECTORY, filename)
            with Image.open(image_path) as image:
                photo_image = ImageTk.PhotoImage(image)
            self.photo_images[filename] = photo_image
        self.set_paddle_images()

    def set_paddle_images(self):
        paddle_image_path = os.path.join(IMAGE_DIRECTORY, PADDLE_FILENAME)
        with Image.open(paddle_image_path) as image:
            self.paddle_image = image.copy()
        laser_paddle_image_path = os.path.join(IMAGE_DIRECTORY, PADDLE_LASERS_FILENAME)
        with Image.open(laser_paddle_image_path) as image:
            self.laser_paddle_image = image.copy()

    def get_paddle(self, paddle: Paddle):
        paddle_pixel_length = paddle.get_length() * PADDLE_WIDTH
        if paddle.is_laser_paddle():
            image = self.laser_paddle_image.copy()
        else:
            image = self.paddle_image.copy()
        image = image.resize((paddle_pixel_length, PADDLE_WIDTH))
        self.photo_images[PADDLE_FILENAME] = ImageTk.PhotoImage(image)
        return self.photo_images[PADDLE_FILENAME]

    def get_brick(self, brick: Brick):
        brick_type = brick.get_type()
        if brick_type == STRONG:
            brick_type = NORMAL
        brick_color = brick.get_color()
        image_key = f'brick-{brick_color}-{brick_type}.png'
        return self.photo_images[image_key]

    def get_background(self):
        return self.photo_images[BACKGROUND_FILENAME]

    def get_powerup(self):
        return self.photo_images[POWERUP_FILENAME]

    def get_laser(self):
        return self.photo_images[LASER_FILENAME]
