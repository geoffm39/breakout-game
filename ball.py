from turtle import RawTurtle

from constants import BALL_START_POSITION, VERTICAL, HORIZONTAL, NORTH, SOUTH, EAST, WEST


class Ball(RawTurtle):
    def __init__(self, canvas, **kwargs):
        super().__init__(canvas, **kwargs)

        self.set_default_ball()

    def set_default_ball(self):
        self.penup()
        self.color('white')
        self.shape('circle')
        self.setposition(BALL_START_POSITION)
        self.setheading(45)

    def move(self):
        self.forward(1)

    def bounce(self, surface):
        if self.is_moving_vertically():
            pass
        elif self.is_moving_west():
            pass
        elif self.is_moving_east():
            pass

    def is_moving_vertically(self):
        direction = self.heading()
        return direction == NORTH or direction == SOUTH

    def is_moving_east(self):
        direction = self.heading()
        return direction < NORTH or direction > SOUTH

    def is_moving_west(self):
        direction = self.heading()
        return direction > NORTH or direction < SOUTH

    @staticmethod
    def is_vertical_surface(surface):
        return surface == VERTICAL

    @staticmethod
    def is_horizontal_surface(surface):
        return surface == HORIZONTAL

    def calculate_vertical_bounce(self, surface):
        if self.is_vertical_surface(surface):
            return
            # todo calculation here
