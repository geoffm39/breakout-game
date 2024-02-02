from turtle import RawTurtle

from constants import SCREEN_WIDTH, PADDLE_START_POSITION


class Paddle(RawTurtle):
    def __init__(self, canvas, **kwargs):
        super().__init__(canvas, **kwargs)

        self.set_default_paddle()

    def move_to(self, x_coord):
        screen_x_coord = x_coord - SCREEN_WIDTH / 2
        self.setx(screen_x_coord)

    def set_default_paddle(self):
        self.penup()
        self.color('blue')
        self.shape('square')
        self.shapesize(stretch_len=5)
        self.setposition(PADDLE_START_POSITION)
