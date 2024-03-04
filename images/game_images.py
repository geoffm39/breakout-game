from PIL import Image, ImageTk, ImageSequence
from tkinter import Canvas
from turtle import RawTurtle
from typing import Union
import os

from brick import Brick
from paddle import Paddle
from laser import Laser
from ball import Ball
from powerup import Powerup
from constants import (
    IMAGE_DIRECTORY, BACKGROUND_FILENAME, POWERUP_FILENAME, PADDLE_FILENAME, BrickType, PowerupType,
    PaddleAttributes, PADDLE_LASERS_FILENAME, LASER_FILENAME, FIREBALL_FILENAME, BALL_FILENAME, LIVES_FILENAME,
    LIVES_IMAGE_Y_COORD, LIVES_IMAGE_X_COORD
)


class GameImages:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas
        self.photo_images = {}
        self.paddle_image = None
        self.laser_paddle_image = None
        self.ball_frames = []
        self.fireball_frames = []

        self.load_images()

    def load_images(self):
        for filename in os.listdir(IMAGE_DIRECTORY):
            image_path = os.path.join(IMAGE_DIRECTORY, filename)
            with Image.open(image_path) as image:
                photo_image = ImageTk.PhotoImage(image)
            self.photo_images[filename] = photo_image
        self.set_paddle_images()
        self.set_ball_frames()
        self.set_fireball_frames()

    def set_paddle_images(self):
        paddle_image_path = os.path.join(IMAGE_DIRECTORY, PADDLE_FILENAME)
        with Image.open(paddle_image_path) as image:
            self.paddle_image = image.copy()
        laser_paddle_image_path = os.path.join(IMAGE_DIRECTORY, PADDLE_LASERS_FILENAME)
        with Image.open(laser_paddle_image_path) as image:
            self.laser_paddle_image = image.copy()

    def apply_background_image(self):
        background = self.get_background()
        self.canvas.create_image(0, 0, image=background)

    def apply_lives_image(self):
        lives = self.get_lives()
        self.canvas.create_image(LIVES_IMAGE_X_COORD, LIVES_IMAGE_Y_COORD, image=lives)

    def create_object_image(self, game_object: Union[Paddle, Ball, Laser, Powerup], frame_index=0):
        object_type = game_object.__class__
        if object_type == Paddle:
            image = self.get_paddle(game_object)
        elif object_type == Ball:
            if game_object.is_fireball():
                image = self.get_fireball_frame(frame_index)
            else:
                image = self.get_ball_frame(frame_index)
        elif object_type == Laser:
            image = self.get_laser()
        elif object_type == Powerup:
            image = self.get_powerup()
        else:
            image = None
        screen_x, screen_y = game_object.get_location()
        canvas_x = screen_x
        canvas_y = screen_y * -1
        canvas_image = self.canvas.create_image(canvas_x, canvas_y, image=image)
        game_object.set_image(canvas_image)

    def move_object_image(self, game_object: Union[Paddle, Ball, Laser, Powerup]):
        object_x, object_y = game_object.get_location()
        self.canvas.coords(game_object.get_image(), (object_x, object_y * -1))

    def update_paddle_image(self, paddle: Paddle):
        updated_image = self.get_paddle(paddle)
        self.canvas.itemconfig(paddle.get_image(), image=updated_image)

    def get_paddle(self, paddle: Paddle):
        paddle_width = PaddleAttributes.WIDTH
        paddle_pixel_length = paddle.get_length() * paddle_width
        if paddle.is_laser_paddle():
            image = self.laser_paddle_image.copy()
        else:
            image = self.paddle_image.copy()
        image = image.resize((paddle_pixel_length, paddle_width))
        self.photo_images[PADDLE_FILENAME] = ImageTk.PhotoImage(image)
        return self.photo_images[PADDLE_FILENAME]

    def get_brick(self, brick: Brick):
        brick_type = brick.get_type()
        if brick_type == BrickType.STRONG:
            brick_type = BrickType.NORMAL
        brick_color = brick.get_color()
        image_key = f'brick-{brick_color}-{brick_type.value}.png'
        return self.photo_images[image_key]

    def set_ball_frames(self):
        ball_image_path = os.path.join(IMAGE_DIRECTORY, BALL_FILENAME)
        with Image.open(ball_image_path) as image:
            self.ball_frames = [ImageTk.PhotoImage(frame.convert('RGBA')) for frame in ImageSequence.Iterator(image)]

    def set_fireball_frames(self):
        fireball_image_path = os.path.join(IMAGE_DIRECTORY, FIREBALL_FILENAME)
        with Image.open(fireball_image_path) as image:
            self.fireball_frames = [ImageTk.PhotoImage(frame.convert('RGBA')) for frame in ImageSequence.Iterator(image)]

    def get_ball_frame(self, frame_index=0):
        frame_index = frame_index % self.get_number_of_ball_frames()
        return self.ball_frames[frame_index]

    def get_fireball_frame(self, frame_index=0):
        frame_index = frame_index % self.get_number_of_fireball_frames()
        return self.fireball_frames[frame_index]

    def get_number_of_ball_frames(self):
        return len(self.ball_frames)

    def get_number_of_fireball_frames(self):
        return len(self.fireball_frames)

    def get_powerup_type(self, powerup_type: PowerupType):
        image_key = f'powerup-{powerup_type.value}.png'
        return self.photo_images[image_key]

    def get_background(self):
        return self.photo_images[BACKGROUND_FILENAME]

    def get_lives(self):
        return self.photo_images[LIVES_FILENAME]

    def get_powerup(self):
        return self.photo_images[POWERUP_FILENAME]

    def get_laser(self):
        return self.photo_images[LASER_FILENAME]
