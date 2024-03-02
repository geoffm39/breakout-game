from turtle import RawTurtle

from constants import (
    TYPE, BRICK_COLOR, BRICK_SHAPE,
    BRICK_WIDTH, BRICK_LENGTH, BrickType, NORMAL_BRICK_SCORE, BROKEN_BRICK_SCORE, STRONG_BRICK_SCORE
)


class Brick(RawTurtle):
    def __init__(self, canvas, brick_attributes: dict, **kwargs):
        super().__init__(canvas, **kwargs)

        self.brick_type = brick_attributes[TYPE]
        self.brick_color = brick_attributes[BRICK_COLOR].value
        self.brick_length = None
        self.brick_location = None
        self.score = self.set_score()

        self.set_properties()

    def set_properties(self):
        self.penup()
        self.shape(BRICK_SHAPE)
        self.shapesize(stretch_len=BRICK_LENGTH)
        self.brick_length = BRICK_WIDTH * BRICK_LENGTH
        self.color(self.brick_color)
        self.hideturtle()

    def set_score(self):
        if self.is_normal():
            return NORMAL_BRICK_SCORE
        elif self.is_broken():
            return BROKEN_BRICK_SCORE
        elif self.is_strong():
            return STRONG_BRICK_SCORE
        else:
            return 0

    def get_score(self):
        return self.score

    def set_location(self, brick_left_x, brick_top_y):
        brick_x = brick_left_x + self.brick_length / 2
        brick_y = brick_top_y - BRICK_WIDTH / 2
        self.brick_location = (brick_x, brick_y)
        self.setposition(self.brick_location)

    def get_length(self):
        return self.brick_length

    def get_color(self):
        return self.brick_color

    def get_location(self):
        return self.brick_location

    def get_bbox(self):
        brick_x, brick_y = self.brick_location
        brick_left_x = brick_x - self.brick_length / 2
        brick_right_x = brick_x + self.brick_length / 2
        brick_top_y = brick_y + BRICK_WIDTH / 2
        brick_bottom_y = brick_y - BRICK_WIDTH / 2
        return brick_left_x, brick_top_y, brick_right_x, brick_bottom_y

    def get_type(self):
        return self.brick_type

    def set_type(self, brick_type: BrickType):
        self.brick_type = brick_type

    def is_normal(self):
        return self.brick_type == BrickType.NORMAL

    def is_strong(self):
        return self.brick_type == BrickType.STRONG

    def is_broken(self):
        return self.brick_type == BrickType.BROKEN

    def is_barrier(self):
        return self.brick_type == BrickType.BARRIER
