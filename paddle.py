from turtle import RawTurtle

from constants import SCREEN_WIDTH


class Paddle(RawTurtle):
    def __init__(self, canvas, **kwargs):
        super().__init__(canvas, **kwargs)

        self.penup()
        self.color('white')
        self.shape('square')
        self.shapesize(stretch_len=5)
        self.setposition((0, -340))

    def move_to(self, x_coord):
        screen_x_coord = x_coord - SCREEN_WIDTH / 2
        self.setx(screen_x_coord)
