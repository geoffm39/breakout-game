from PIL import Image, ImageTk, ImageSequence
from tkinter import Canvas
from typing import Union
import os

from brick import Brick
from paddle import Paddle
from laser import Laser
from ball import Ball
from powerup import Powerup
from constants import (
    BrickType, PowerupType, FilePaths, PaddleAttributes, BallAttributes, PowerupAttributes,
    TextAttributes, SCREEN_HEIGHT, SCREEN_CENTER
)


class GameImages:
    def __init__(self, canvas: Canvas):
        self.canvas = canvas
        self.photo_images = {}
        self.paddle_image = None
        self.laser_paddle_image = None
        self.ball_frames = []
        self.fireball_frames = []
        self.powerup_type_images = []

        self.load_images()

    def load_images(self):
        for filename in os.listdir(FilePaths.IMAGE_DIRECTORY):
            image_path = os.path.join(FilePaths.IMAGE_DIRECTORY, filename)
            with Image.open(image_path) as image:
                photo_image = ImageTk.PhotoImage(image)
            self.photo_images[filename] = photo_image
        self.set_paddle_images()
        self.set_ball_frames()
        self.set_fireball_frames()

    def set_paddle_images(self):
        paddle_image_path = os.path.join(FilePaths.IMAGE_DIRECTORY, FilePaths.PADDLE)
        with Image.open(paddle_image_path) as image:
            self.paddle_image = image.copy()
        laser_paddle_image_path = os.path.join(FilePaths.IMAGE_DIRECTORY, FilePaths.PADDLE_LASERS)
        with Image.open(laser_paddle_image_path) as image:
            self.laser_paddle_image = image.copy()

    def apply_background_image(self):
        background = self.get_background()
        x, y = SCREEN_CENTER
        self.canvas.create_image(x, y, image=background)

    def apply_lives_image(self):
        lives = self.get_lives()
        self.canvas.create_image(TextAttributes.LIVES_IMAGE_X_COORD,
                                 TextAttributes.LIVES_IMAGE_Y_COORD,
                                 image=lives)

    def handle_game_over_images(self):
        self.show_game_over_image()
        self.show_quit_button_images()

    def show_game_over_image(self):
        game_over_image = self.get_game_over()
        x, y = SCREEN_CENTER
        self.canvas.create_image(x, y, image=game_over_image)

    def show_quit_button_images(self):
        button_image = self.get_button_outline()
        yes_x, yes_y = TextAttributes.YES_BUTTON_OUTLINE_POSITION
        no_x, no_y = TextAttributes.NO_BUTTON_OUTLINE_POSITION
        self.canvas.create_image(yes_x, yes_y, image=button_image, anchor='s')
        self.canvas.create_image(no_x, no_y, image=button_image, anchor='s')

    def create_object_image(self, game_object: Union[Paddle, Ball, Laser, Powerup, Brick]):
        image = self.get_object_image(game_object)
        screen_x, screen_y = game_object.get_location()
        canvas_x = screen_x
        canvas_y = screen_y * -1
        canvas_image = self.canvas.create_image(canvas_x, canvas_y, image=image)
        game_object.set_image(canvas_image)

    def move_object_image(self, game_object: Union[Paddle, Ball, Laser, Powerup, Brick]):
        object_x, object_y = game_object.get_location()
        self.canvas.coords(game_object.get_image(), (object_x, object_y * -1))

    def delete_object_image(self, game_object: Union[Paddle, Ball, Laser, Powerup, Brick]):
        self.canvas.delete(game_object.get_image())

    def update_object_image(self, game_object: Union[Paddle, Ball, Laser, Powerup, Brick]):
        updated_image = self.get_object_image(game_object)
        self.canvas.itemconfig(game_object.get_image(), image=updated_image)

    def add_ball_animation(self, ball: Ball):
        self.create_object_image(ball)
        self.cycle_ball_animation_frames(ball)

    def cycle_ball_animation_frames(self, ball: Ball, frame_index=0):
        if ball:
            if ball.is_fireball():
                frame_index = (frame_index + 1) % self.get_number_of_fireball_frames()
                frame = self.get_fireball_frame(frame_index)
            else:
                frame_index = (frame_index + 1) % self.get_number_of_ball_frames()
                frame = self.get_ball_frame(frame_index)
            self.canvas.itemconfig(ball.get_image(), image=frame)
            self.canvas.after(BallAttributes.ANIMATION_SPEED, self.cycle_ball_animation_frames, ball, frame_index)

    def get_object_image(self, game_object: Union[Paddle, Ball, Laser, Powerup, Brick]):
        object_type = game_object.__class__
        if object_type == Paddle:
            image = self.get_paddle(game_object)
        elif object_type == Ball:
            if game_object.is_fireball():
                image = self.get_fireball_frame()
            else:
                image = self.get_ball_frame()
        elif object_type == Laser:
            image = self.get_laser()
        elif object_type == Powerup:
            image = self.get_powerup()
        elif object_type == Brick:
            image = self.get_brick(game_object)
        else:
            image = None
        return image

    def add_powerup_type_image(self, powerup_type: PowerupType, paddle: Paddle):
        image = self.get_powerup_type(powerup_type)
        canvas_x = paddle.xcor()
        canvas_y = SCREEN_HEIGHT / 2 - 50
        canvas_image = self.canvas.create_image(canvas_x, canvas_y, image=image)
        self.powerup_type_images.append(canvas_image)
        self.canvas.after(PowerupAttributes.IMAGE_TIME_LIMIT, lambda: self.remove_powerup_type_image(canvas_image))

    def move_powerup_type_image(self, canvas_image):
        if canvas_image:
            self.canvas.move(canvas_image, 0, PowerupAttributes.IMAGE_SPEED)

    def remove_powerup_type_image(self, canvas_image):
        self.canvas.delete(canvas_image)
        self.powerup_type_images.remove(canvas_image)

    def get_powerup_type_images(self):
        return self.powerup_type_images

    def get_paddle(self, paddle: Paddle):
        paddle_width = PaddleAttributes.WIDTH
        paddle_pixel_length = paddle.get_length() * paddle_width
        if paddle.is_laser_paddle():
            image = self.laser_paddle_image.copy()
        else:
            image = self.paddle_image.copy()
        image = image.resize((paddle_pixel_length, paddle_width))
        self.photo_images[FilePaths.PADDLE] = ImageTk.PhotoImage(image)
        return self.photo_images[FilePaths.PADDLE]

    def get_brick(self, brick: Brick):
        brick_type = brick.get_type()
        if brick_type == BrickType.STRONG:
            brick_type = BrickType.NORMAL
        brick_color = brick.get_color()
        image_key = f'brick-{brick_color}-{brick_type.value}.png'
        return self.photo_images[image_key]

    def set_ball_frames(self):
        ball_image_path = os.path.join(FilePaths.IMAGE_DIRECTORY, FilePaths.BALL)
        with Image.open(ball_image_path) as image:
            self.ball_frames = [ImageTk.PhotoImage(frame.convert('RGBA')) for frame in ImageSequence.Iterator(image)]

    def set_fireball_frames(self):
        fireball_image_path = os.path.join(FilePaths.IMAGE_DIRECTORY, FilePaths.FIREBALL)
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
        return self.photo_images[FilePaths.BACKGROUND]

    def get_lives(self):
        return self.photo_images[FilePaths.LIVES]

    def get_game_over(self):
        return self.photo_images[FilePaths.GAME_OVER]

    def get_powerup(self):
        return self.photo_images[FilePaths.POWERUP]

    def get_laser(self):
        return self.photo_images[FilePaths.LASER]

    def get_button_outline(self):
        return self.photo_images[FilePaths.BUTTON_OUTLINE]
