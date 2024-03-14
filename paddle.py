from turtle import RawTurtle

from constants import SCREEN_WIDTH, PaddleAttributes, SCREEN_LEFT_EDGE, SCREEN_RIGHT_EDGE


class Paddle(RawTurtle):
    def __init__(self, screen, **kwargs):
        super().__init__(screen, **kwargs)

        self.screen = screen
        self.paddle_length = PaddleAttributes.DEFAULT_LENGTH
        self.lasers = False
        self.image = None
        self.moving = False

        self.set_default_paddle()

    def move_to(self, x_coord):
        screen_x_coord = x_coord - SCREEN_WIDTH / 2
        if not self.paddle_reached_screen_edge(screen_x_coord):
            self.setx(screen_x_coord)

    def move_left(self):
        x_coord = self.xcor() - PaddleAttributes.MOVEMENT
        if not self.paddle_reached_screen_edge(x_coord):
            self.setx(x_coord)
        else:
            self.setx(SCREEN_LEFT_EDGE + self.paddle_length * PaddleAttributes.WIDTH / 2)

    def move_right(self):
        x_coord = self.xcor() + PaddleAttributes.MOVEMENT
        if not self.paddle_reached_screen_edge(x_coord):
            self.setx(x_coord)
        else:
            self.setx(SCREEN_RIGHT_EDGE - self.paddle_length * PaddleAttributes.WIDTH / 2)

    def is_moving(self):
        return self.moving

    def set_moving(self, moving: bool):
        self.moving = moving

    def paddle_reached_screen_edge(self, x_coord):
        left_x_loc, right_x_loc = self.get_x_coordinates(x_coord)
        return left_x_loc < SCREEN_LEFT_EDGE or right_x_loc > SCREEN_RIGHT_EDGE

    def set_default_paddle(self):
        self.penup()
        self.color(PaddleAttributes.COLOR)
        self.shape(PaddleAttributes.SHAPE)
        self.shapesize(stretch_len=self.paddle_length)
        self.setposition(PaddleAttributes.START_POSITION)
        self.hideturtle()

    def set_image(self, canvas_image):
        self.image = canvas_image

    def get_image(self):
        return self.image

    def get_x_coordinates(self, x_coord=None):
        if x_coord:
            paddle_x_loc = x_coord
        else:
            paddle_x_loc = self.xcor()
        paddle_pixel_length = PaddleAttributes.WIDTH * self.paddle_length
        left_x_loc = paddle_x_loc - paddle_pixel_length / 2
        right_x_loc = paddle_x_loc + paddle_pixel_length / 2
        return left_x_loc, right_x_loc

    def get_bbox(self):
        paddle_x, paddle_y = self.xcor(), self.ycor()
        paddle_width = PaddleAttributes.WIDTH
        paddle_left_x, paddle_right_x = self.get_x_coordinates()
        paddle_bbox = (paddle_left_x, paddle_y + paddle_width / 2, paddle_right_x, paddle_y - paddle_width / 2)
        return paddle_bbox

    def get_location(self) -> tuple:
        x_location = self.xcor()
        y_location = self.ycor()
        return x_location, y_location

    def get_length(self):
        return self.paddle_length

    def activate_lasers(self):
        self.lasers = True
        self.color(PaddleAttributes.LASER_PADDLE_COLOR)

    def deactivate_lasers(self):
        self.lasers = False
        self.color(PaddleAttributes.COLOR)

    def is_laser_paddle(self):
        return self.lasers

    def get_modifier_angle(self, paddle_collision_x_coord):
        paddle_x1, _, paddle_x2, _ = self.get_bbox()
        paddle_pixel_length = self.paddle_length * PaddleAttributes.WIDTH
        paddle_centre_x = paddle_x1 + paddle_pixel_length/2
        relative_position = paddle_centre_x - paddle_collision_x_coord
        normalised_position = relative_position / (paddle_pixel_length / 2)
        modifier_angle = normalised_position * 90
        return modifier_angle

    def increase_size(self):
        if self.paddle_length <= 10:
            self.paddle_length += 1
        self.shapesize(stretch_len=self.paddle_length)

    def decrease_size(self):
        if self.paddle_length > 1:
            self.paddle_length -= 1
        self.shapesize(stretch_len=self.paddle_length)

    def reset_size(self):
        self.paddle_length = PaddleAttributes.DEFAULT_LENGTH
        self.shapesize(stretch_len=self.paddle_length)
