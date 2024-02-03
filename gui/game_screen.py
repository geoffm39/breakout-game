from tkinter import *
from turtle import TurtleScreen

from paddle import Paddle
from ball import Ball
from bricks import Bricks
from powerup import Powerup
from scores import Scores
from constants import VERTICAL_SURFACE, HORIZONTAL_SURFACE


class GameScreen(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(background='black')

        self.screen = TurtleScreen(self)
        self.configure_screen()

        self.paddle = Paddle(self.screen)
        self.ball = Ball(self.screen)

        self.apply_mouse_controls()

    def apply_mouse_controls(self):
        self.bind('<Motion>', self.track_player_movement)
        self.bind('<Enter>', self.hide_mouse_cursor)
        self.bind('<Leave>', self.show_mouse_cursor)

    def track_player_movement(self, event):
        x = event.x
        self.paddle.move_to(x)
        # self.screen.update()

    def hide_mouse_cursor(self, event):
        self.config(cursor='none')

    def show_mouse_cursor(self, event):
        self.config(cursor='')

    def configure_screen(self):
        self.screen.tracer(0)
        self.screen.bgcolor('black')
        self.screen.listen()

    def start_game(self):
        self.update_game_screen()

    def update_game_screen(self):
        self.screen.update()
        self.ball.move()
        if self.ball.ycor() >= 360 or self.ball.ycor() <= -360:
            self.ball.bounce(HORIZONTAL_SURFACE)
        if self.ball.xcor() >= 540 or self.ball.xcor() <= -540:
            self.ball.bounce(VERTICAL_SURFACE)

        self.after(3, self.update_game_screen)
