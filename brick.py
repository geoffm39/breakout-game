from turtle import Turtle

from constants import (
    BRICK_LOCATION, TYPE, NORMAL, STRONG, BARRIER, BRICK_COLOR, BRICK_SHAPE,
    BRICK_WIDTH, BRICK_LENGTH, BARRIER_LENGTH
)


class Brick(Turtle):
    def __init__(self, brick_attributes: dict, **kwargs):
        super().__init__(**kwargs)

        self.brick_type = brick_attributes[TYPE]
        self.brick_color = brick_attributes[BRICK_COLOR]
        self.brick_length = None
        self.brick_location = None

        self.set_brick_properties()

    def set_brick_properties(self):
        self.penup()
        self.shape(BRICK_SHAPE)
        if self.is_barrier():
            self.shapesize(stretch_len=BARRIER_LENGTH)
            self.brick_length = BRICK_WIDTH * BARRIER_LENGTH
        else:
            self.shapesize(stretch_len=BRICK_LENGTH)
            self.brick_length = BRICK_WIDTH * BRICK_LENGTH
        self.color(self.brick_color)

    def set_brick_location(self, brick_left_x, brick_top_y):
        brick_x = brick_left_x + self.brick_length / 2
        brick_y = brick_top_y - BRICK_WIDTH / 2
        self.brick_location = (brick_x, brick_y)
        self.setposition(self.brick_location)

    def get_brick_length(self):
        return self.brick_length

    def get_brick_bbox(self):
        brick_x, brick_y = self.brick_location
        brick_left_x = brick_x - self.brick_length / 2
        brick_right_x = brick_x + self.brick_length / 2
        brick_top_y = brick_y + BRICK_WIDTH / 2
        brick_bottom_y = brick_y - BRICK_WIDTH / 2
        return brick_left_x, brick_top_y, brick_right_x, brick_bottom_y

    def is_barrier(self):
        return self.brick_type == BARRIER

    def is_normal(self):
        return self.brick_type == NORMAL

    def is_strong(self):
        return self.brick_type == STRONG
