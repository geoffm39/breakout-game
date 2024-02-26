from PIL import Image, ImageTk, ImageSequence
import os

from brick import Brick
from paddle import Paddle
from constants import (
    IMAGE_DIRECTORY, STRONG, NORMAL, BACKGROUND_FILENAME, POWERUP_FILENAME, PADDLE_FILENAME,
    PADDLE_WIDTH, PADDLE_LASERS_FILENAME, LASER_FILENAME, PowerupType, FIREBALL_FILENAME
)


class GameImages:
    def __init__(self):
        self.photo_images = {}
        self.paddle_image = None
        self.laser_paddle_image = None
        self.fireball_frames = []

        self.load_images()

    def load_images(self):
        for filename in os.listdir(IMAGE_DIRECTORY):
            image_path = os.path.join(IMAGE_DIRECTORY, filename)
            with Image.open(image_path) as image:
                photo_image = ImageTk.PhotoImage(image)
            self.photo_images[filename] = photo_image
        self.set_paddle_images()
        self.set_fireball_frames()

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

    def set_fireball_frames(self):
        fireball_image_path = os.path.join(IMAGE_DIRECTORY, FIREBALL_FILENAME)
        with Image.open(fireball_image_path) as image:
            self.fireball_frames = [ImageTk.PhotoImage(frame.convert('RGBA')) for frame in ImageSequence.Iterator(image)]
            # FRAMES ALL THE SAME HERE!! FIX

    def get_fireball_frame(self, frame_index=0):
        frame_index = frame_index % len(self.fireball_frames)
        return self.fireball_frames[frame_index]

    def get_number_of_fireball_frames(self):
        return len(self.fireball_frames)

    def get_powerup_type(self, powerup_type: PowerupType):
        image_key = f'powerup-{powerup_type.value}.png'
        return self.photo_images[image_key]

    def get_background(self):
        return self.photo_images[BACKGROUND_FILENAME]

    def get_powerup(self):
        return self.photo_images[POWERUP_FILENAME]

    def get_laser(self):
        return self.photo_images[LASER_FILENAME]
