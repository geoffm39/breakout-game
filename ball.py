from turtle import RawTurtle
from random import randint

from constants import (
    BallAttributes, VERTICAL_SURFACE, HORIZONTAL_SURFACE,
    NORTH, SOUTH, EAST, WEST, COMPLETE_ANGLE, PaddleAttributes, Color
)


class Ball(RawTurtle):
    def __init__(self, canvas, **kwargs):
        super().__init__(canvas, **kwargs)

        self.move_speed = BallAttributes.DEFAULT_SPEED
        self.fireball = False
        self.latest_barrier_hit = None

        self.set_default_ball()

    def set_default_ball(self):
        self.penup()
        self.color(BallAttributes.COLOR)
        self.shape(BallAttributes.SHAPE)
        self.setposition(BallAttributes.START_POSITION)
        self.set_random_starting_direction()
        self.hideturtle()

    def set_random_starting_direction(self):
        min_angle = EAST + 20
        max_angle = WEST - 20
        random_angle = randint(min_angle, max_angle)
        self.setheading(random_angle)

    def move(self):
        self.forward(self.move_speed)

    def get_bbox(self):
        ball_x, ball_y = self.xcor(), self.ycor()
        ball_radius = BallAttributes.RADIUS
        return ball_x - ball_radius, ball_y + ball_radius, ball_x + ball_radius, ball_y - ball_radius

    def get_location(self):
        ball_x, ball_y = self.xcor(), self.ycor()
        return ball_x, ball_y

    def get_direction(self):
        return self.heading()

    def bounce(self, surface, paddle_angle_modifier=None):
        direction = self.get_direction()
        if self.is_moving_vertically(direction):
            reflection_angle = self.calculate_vertical_movement(direction, surface)
        elif self.is_moving_north_east(direction):
            reflection_angle = self.calculate_north_east_movement(direction, surface)
        elif self.is_moving_north_west(direction):
            reflection_angle = self.calculate_north_west_movement(direction, surface)
        elif self.is_moving_south_west(direction):
            reflection_angle = self.calculate_south_west_movement(direction, surface)
        elif self.is_moving_south_east(direction):
            reflection_angle = self.calculate_south_east_movement(direction, surface)
        else:
            print('bounce error')
            return  # add error throw here
        if paddle_angle_modifier:
            modified_paddle_angle = reflection_angle + paddle_angle_modifier
            reflection_angle = self.clamp_angle_to_reflection_range(modified_paddle_angle)
        self.set_direction(reflection_angle)

    def set_latest_barrier_hit(self, brick):
        self.latest_barrier_hit = brick

    def get_latest_barrier_hit(self):
        return self.latest_barrier_hit

    def clear_latest_barrier_hit(self):
        self.latest_barrier_hit = None

    @staticmethod
    def clamp_angle_to_reflection_range(angle):
        return max(min(angle, PaddleAttributes.MAX_ANGLE), PaddleAttributes.MIN_ANGLE)

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
        return surface == VERTICAL_SURFACE

    @staticmethod
    def is_horizontal_surface(surface):
        return surface == HORIZONTAL_SURFACE

    def calculate_vertical_movement(self, direction, surface):
        if self.is_vertical_surface(surface):
            return direction
        if direction == NORTH:
            return SOUTH
        else:
            return NORTH

    def calculate_north_east_movement(self, direction, surface):
        if self.is_horizontal_surface(surface):
            incidence_angle = direction
            reflection_angle = COMPLETE_ANGLE - incidence_angle
        else:
            incidence_angle = NORTH - direction
            reflection_angle = NORTH + incidence_angle
        return reflection_angle

    def calculate_north_west_movement(self, direction, surface):
        if self.is_horizontal_surface(surface):
            incidence_angle = WEST - direction
            reflection_angle = WEST + incidence_angle
        else:
            incidence_angle = direction - NORTH
            reflection_angle = NORTH - incidence_angle
        return reflection_angle

    def calculate_south_west_movement(self, direction, surface):
        if self.is_horizontal_surface(surface):
            incidence_angle = direction - WEST
            reflection_angle = WEST - incidence_angle
        else:
            incidence_angle = SOUTH - direction
            reflection_angle = SOUTH + incidence_angle
        return reflection_angle

    def calculate_south_east_movement(self, direction, surface):
        if self.is_horizontal_surface(surface):
            incidence_angle = COMPLETE_ANGLE - direction
            reflection_angle = incidence_angle
        else:
            incidence_angle = direction - SOUTH
            reflection_angle = SOUTH - incidence_angle
        return reflection_angle

    def set_direction(self, direction):
        self.setheading(direction)

    def increase_speed(self):
        self.move_speed += 0.25

    def decrease_speed(self):
        if self.move_speed > 0.5:
            self.move_speed -= 0.25

    def get_speed(self):
        return self.move_speed

    def set_speed(self, speed):
        self.move_speed = speed

    def reset_speed(self):
        self.move_speed = BallAttributes.DEFAULT_SPEED

    def activate_fireball(self):
        self.fireball = True
        self.color(Color.RED.value)

    def is_fireball(self):
        return self.fireball

    def remove(self):
        self.hideturtle()
