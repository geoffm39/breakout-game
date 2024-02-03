from turtle import RawTurtle

from constants import BALL_START_POSITION, VERTICAL, HORIZONTAL, NORTH, SOUTH, EAST, WEST, COMPLETE_ANGLE


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
        direction = self.heading()
        if self.is_moving_vertically(direction):
            self.calculate_vertical_movement(direction, surface)
        elif self.is_moving_north_east(direction):
            self.calculate_north_east_movement(direction, surface)
        elif self.is_moving_north_west(direction):
            self.calculate_north_west_movement(direction, surface)
        elif self.is_moving_south_west(direction):
            self.calculate_south_west_movement(direction, surface)
        elif self.is_moving_south_east(direction):
            self.calculate_south_east_movement(direction, surface)

    @staticmethod
    def is_moving_vertically(direction):
        return direction == NORTH or direction == SOUTH

    @staticmethod
    def is_moving_north_east(direction):
        return EAST < direction < NORTH

    @staticmethod
    def is_moving_north_west(direction):
        return NORTH < direction < WEST

    @staticmethod
    def is_moving_south_west(direction):
        return WEST < direction < SOUTH

    @staticmethod
    def is_moving_south_east(direction):
        return SOUTH < direction

    @staticmethod
    def is_vertical_surface(surface):
        return surface == VERTICAL

    @staticmethod
    def is_horizontal_surface(surface):
        return surface == HORIZONTAL

    def calculate_vertical_movement(self, direction, surface):
        if self.is_vertical_surface(surface):
            return
        if self.heading() == NORTH:
            self.set_ball_direction(SOUTH)
        else:
            self.set_ball_direction(NORTH)

    def calculate_north_east_movement(self, direction, surface):
        if self.is_horizontal_surface(surface):
            incidence_angle = direction
            reflection_angle = COMPLETE_ANGLE - incidence_angle
            self.set_ball_direction(reflection_angle)
        else:
            incidence_angle = NORTH - direction
            reflection_angle = NORTH + incidence_angle
            self.set_ball_direction(reflection_angle)

    def calculate_north_west_movement(self, direction, surface):
        if self.is_horizontal_surface(surface):
            incidence_angle = WEST - direction
            reflection_angle = WEST + incidence_angle
            self.set_ball_direction(reflection_angle)
        else:
            incidence_angle = direction - NORTH
            reflection_angle = NORTH - incidence_angle
            self.set_ball_direction(reflection_angle)

    def calculate_south_west_movement(self, direction, surface):
        if self.is_horizontal_surface(surface):
            incidence_angle = direction - WEST
            reflection_angle = WEST - incidence_angle
            self.set_ball_direction(reflection_angle)
        else:
            incidence_angle = SOUTH - direction
            reflection_angle = SOUTH + incidence_angle
            self.set_ball_direction(reflection_angle)

    def calculate_south_east_movement(self, direction, surface):
        if self.is_horizontal_surface(surface):
            incidence_angle = COMPLETE_ANGLE - direction
            reflection_angle = incidence_angle
            self.set_ball_direction(reflection_angle)
        else:
            incidence_angle = direction - SOUTH
            reflection_angle = SOUTH - incidence_angle
            self.set_ball_direction(reflection_angle)

    def set_ball_direction(self, direction):
        self.setheading(direction)
