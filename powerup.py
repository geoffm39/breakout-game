from turtle import RawTurtle

from constants import (
   PowerupType, POWERUP_SHAPE, POWERUP_COLOR, POWERUP_SPEED, SOUTH
)


class Powerup(RawTurtle):
    def __init__(self, canvas, powerup_type, location, **kwargs):
        super().__init__(canvas, **kwargs)

        self.type = powerup_type
        self.location = location

        self.set_properties()

    def set_properties(self):
        self.penup()
        self.shape(POWERUP_SHAPE)
        self.color(POWERUP_COLOR)
        self.setheading(SOUTH)
        self.setposition(self.location)
        # self.hideturtle()

    def move(self):
        self.forward(POWERUP_SPEED)

    def remove(self):
        self.hideturtle()

    def get_type(self):
        return self.type
