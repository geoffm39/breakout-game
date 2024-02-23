from turtle import RawTurtle

from constants import (
    LASER_COLOR, LASER_SHAPE, LASER_SPEED, NORTH
)


class Laser(RawTurtle):
    def __init__(self, canvas, location, **kwargs):
        super().__init__(canvas, **kwargs)

        self.location = location

        self.set_default_laser()

    def set_default_laser(self):
        self.penup()
        self.color(LASER_COLOR)
        self.shape(LASER_SHAPE)
        self.setheading(NORTH)
        self.setposition(self.location)
        self.hideturtle()

    def move(self):
        self.forward(LASER_SPEED)

    def remove(self):
        self.hideturtle()

    def get_location(self):
        return self.location
