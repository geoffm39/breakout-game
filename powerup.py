from turtle import RawTurtle

from constants import PowerupType, SOUTH, PowerupAttributes


class Powerup(RawTurtle):
    def __init__(self, canvas, powerup_type: PowerupType, location, **kwargs):
        super().__init__(canvas, **kwargs)

        self.type = powerup_type
        self.location = location
        self.image = None

        self.set_default_powerup()

    def set_default_powerup(self):
        self.penup()
        self.shape(PowerupAttributes.SHAPE)
        self.color(PowerupAttributes.COLOR)
        self.setheading(SOUTH)
        self.setposition(self.location)
        self.hideturtle()

    def set_image(self, canvas_image):
        self.image = canvas_image

    def get_image(self):
        return self.image

    def move(self):
        self.forward(PowerupAttributes.SPEED)

    def remove(self):
        self.hideturtle()

    def get_type(self):
        return self.type

    def get_location(self):
        return self.location
