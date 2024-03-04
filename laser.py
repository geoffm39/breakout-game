from turtle import RawTurtle

from constants import NORTH, LaserAttributes


class Laser(RawTurtle):
    def __init__(self, canvas, location, **kwargs):
        super().__init__(canvas, **kwargs)

        self.location = location
        self.image = None

        self.set_default_laser()

    def set_default_laser(self):
        self.penup()
        self.color(LaserAttributes.COLOR)
        self.shape(LaserAttributes.SHAPE)
        self.setheading(NORTH)
        self.setposition(self.location)
        self.hideturtle()

    def set_image(self, canvas_image):
        self.image = canvas_image

    def get_image(self):
        return self.image

    def move(self):
        self.forward(LaserAttributes.SPEED)

    def remove(self):
        self.hideturtle()

    def get_location(self):
        return self.xcor(), self.ycor()

    def get_bbox(self):
        laser_x, laser_y = self.xcor(), self.ycor()
        laser_width = LaserAttributes.WIDTH
        laser_x1 = laser_x - laser_width / 4
        laser_y1 = laser_y + laser_width / 2
        laser_x2 = laser_x + laser_width / 4
        laser_y2 = laser_y - laser_width / 2
        return laser_x1, laser_y1, laser_x2, laser_y2
