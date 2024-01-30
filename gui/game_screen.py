from tkinter import *

from paddle import Paddle
from ball import Ball
from bricks import Bricks
from powerup import Powerup
from scores import Scores


class GameScreen(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(background='black')

        self.paddle = Paddle(self)

        self.screen = self.paddle.getscreen()
        self.screen.tracer(0)
        self.screen.bgcolor('black')
        self.screen.listen()

        self.bind('<Motion>', self.track_player_movement)
        self.bind('<Enter>', self.hide_mouse_cursor)
        self.bind('<Leave>', self.show_mouse_cursor)

    def track_player_movement(self, event):
        x = event.x
        self.paddle.move_to(x)
        self.screen.update()

    def hide_mouse_cursor(self, event):
        self.config(cursor='none')

    def show_mouse_cursor(self, event):
        self.config(cursor='')
