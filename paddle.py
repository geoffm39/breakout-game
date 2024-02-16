from turtle import RawTurtle

from constants import (
    SCREEN_WIDTH, PADDLE_START_POSITION, PADDLE_LENGTH, PADDLE_WIDTH,
    SCREEN_LEFT_EDGE, SCREEN_RIGHT_EDGE, PADDLE_COLOR, PADDLE_SHAPE
)


class Paddle(RawTurtle):
    def __init__(self, canvas, **kwargs):
        super().__init__(canvas, **kwargs)

        self.paddle_length = PADDLE_LENGTH

        self.set_default_paddle()

    def move_to(self, x_coord):
        screen_x_coord = x_coord - SCREEN_WIDTH / 2
        if not self.paddle_reached_screen_edge(screen_x_coord):
            self.setx(screen_x_coord)

    def paddle_reached_screen_edge(self, x_coord):
        left_x_loc, right_x_loc = self.get_x_coordinates(x_coord)
        return left_x_loc < SCREEN_LEFT_EDGE or right_x_loc > SCREEN_RIGHT_EDGE

    def set_default_paddle(self):
        self.penup()
        self.color(PADDLE_COLOR)
        self.shape(PADDLE_SHAPE)
        self.shapesize(stretch_len=self.paddle_length)
        self.setposition(PADDLE_START_POSITION)

    def get_x_coordinates(self, x_coord=None):
        if x_coord:
            paddle_x_loc = x_coord
        else:
            paddle_x_loc = self.xcor()
        paddle_pixel_length = PADDLE_WIDTH * self.paddle_length
        left_x_loc = paddle_x_loc - paddle_pixel_length / 2
        right_x_loc = paddle_x_loc + paddle_pixel_length / 2
        return left_x_loc, right_x_loc

    def get_bbox(self):
        paddle_x, paddle_y = self.xcor(), self.ycor()
        paddle_left_x, paddle_right_x = self.get_x_coordinates()
        paddle_bbox = (paddle_left_x, paddle_y + PADDLE_WIDTH / 2, paddle_right_x, paddle_y - PADDLE_WIDTH / 2)
        return paddle_bbox

    def get_modifier_angle(self, paddle_contact_x_coord):
        paddle_x1, _, paddle_x2, _ = self.get_bbox()
        paddle_pixel_length = self.paddle_length * PADDLE_WIDTH
        paddle_centre_x = paddle_x1 + paddle_pixel_length/2
        relative_position = paddle_centre_x - paddle_contact_x_coord
        normalised_position = relative_position / (paddle_pixel_length / 2)
        modifier_angle = normalised_position * 90
        return modifier_angle
