from turtle import RawTurtle

from constants import (
    SCREEN_WIDTH, PADDLE_START_POSITION, PADDLE_LENGTH, PADDLE_WIDTH,
    SCREEN_LEFT_EDGE, SCREEN_RIGHT_EDGE
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
        left_x_loc, right_x_loc = self.get_paddle_x_coordinates(x_coord)
        return left_x_loc < SCREEN_LEFT_EDGE or right_x_loc > SCREEN_RIGHT_EDGE

    def set_default_paddle(self):
        self.penup()
        self.color('blue')
        self.shape('square')
        self.shapesize(stretch_len=self.paddle_length)
        self.setposition(PADDLE_START_POSITION)

    def get_paddle_x_coordinates(self, x_coord=None):
        if x_coord:
            paddle_x_loc = x_coord
        else:
            paddle_x_loc = self.xcor()
        paddle_pixel_length = PADDLE_WIDTH * PADDLE_LENGTH
        left_x_loc = paddle_x_loc - paddle_pixel_length / 2
        right_x_loc = paddle_x_loc + paddle_pixel_length / 2
        return left_x_loc, right_x_loc
