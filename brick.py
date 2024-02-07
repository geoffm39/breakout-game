from turtle import RawTurtle

from constants import (
    BRICK_LOCATION, BRICK_TYPE, BRICK_COLOR, BRICK_SHAPE,
    BRICK_WIDTH, BRICK_LENGTH, BARRIER_WIDTH, BARRIER_LENGTH
)


class Brick(RawTurtle):
    def __init__(self, canvas, brick_attributes: dict, **kwargs):
        super().__init__(canvas, **kwargs)

        self.brick_type = brick_attributes[BRICK_TYPE]
        self.brick_color = brick_attributes[BRICK_COLOR]
        self.brick_location = brick_attributes[BRICK_LOCATION]

    def setup_brick(self):
        self.penup()
        self.shape(BRICK_SHAPE)
        self.color(self.brick_color)
