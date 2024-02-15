from tkinter import *
from turtle import TurtleScreen

from paddle import Paddle
from ball import Ball
from brick import Brick
from powerup import Powerup
from scores import Scores
from levels import Levels
from constants import (
    VERTICAL_SURFACE, HORIZONTAL_SURFACE, BALL_RADIUS, BRICK_SPACING, TYPE, SPACING, SPACE_SIZE, BRICK_WIDTH,
    SCREEN_BOTTOM_EDGE, SCREEN_TOP_EDGE, SCREEN_RIGHT_EDGE, SCREEN_LEFT_EDGE, BALL_SPEED
)


class GameScreen(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(background='black')

        self.screen = TurtleScreen(self)
        self.configure_screen()

        self.paddle = Paddle(self.screen)
        self.levels = Levels()
        self.bricks = []
        self.balls = []

        self.current_level = 1
        self.apply_mouse_controls()

    def apply_mouse_controls(self):
        self.bind('<Motion>', self.track_player_movement)
        self.bind('<Enter>', self.hide_mouse_cursor)
        self.bind('<Leave>', self.show_mouse_cursor)

    def track_player_movement(self, event):
        x = event.x
        self.paddle.move_to(x)

    def hide_mouse_cursor(self, event):
        self.config(cursor='none')

    def show_mouse_cursor(self, event):
        self.config(cursor='')

    def configure_screen(self):
        self.screen.tracer(0)
        self.screen.bgcolor('black')
        self.screen.listen()

    def start_game(self):
        self.add_level_bricks()
        self.balls.append(Ball(self.screen))
        self.update_game_screen()

    def add_level_bricks(self):
        level_data = self.levels.get_level(self.current_level)
        y_location = SCREEN_TOP_EDGE - BRICK_SPACING
        for row in level_data:
            x_location = SCREEN_LEFT_EDGE + BRICK_SPACING
            for item in row:
                if self.is_spacing(item):
                    x_location += item[SPACE_SIZE]
                    x_location += BRICK_SPACING
                else:
                    new_brick = Brick(self.screen, item)
                    new_brick.set_brick_location(x_location, y_location)
                    self.bricks.append(new_brick)
                    x_location += new_brick.get_brick_length()
                    x_location += BRICK_SPACING
            y_location -= BRICK_WIDTH
            y_location -= BRICK_SPACING

    @staticmethod
    def is_spacing(position):
        return position[TYPE] == SPACING

    def update_game_screen(self):
        self.screen.update()
        for ball in self.balls:
            ball.move()
            self.check_for_ball_contact(ball)
            if self.ball_missed(ball):
                return
        self.after(3, self.update_game_screen)

    def check_for_ball_contact(self, ball: Ball):
        self.check_for_paddle_contact(ball)
        self.check_for_brick_contact(ball)
        self.check_for_wall_contact(ball)

    def check_for_wall_contact(self, ball: Ball):
        if self.ball_hit_side_wall(ball):
            ball.bounce(VERTICAL_SURFACE)
        if self.ball_hit_top_wall(ball):
            ball.bounce(HORIZONTAL_SURFACE)

    def check_for_paddle_contact(self, ball: Ball):
        paddle_bbox = self.paddle.get_paddle_bbox()
        if self.ball_hit_paddle(ball, paddle_bbox):
            paddle_angle_modifier = self.paddle.get_paddle_modifier_angle(ball.xcor())
            ball.bounce(HORIZONTAL_SURFACE, paddle_angle_modifier)

    def check_for_brick_contact(self, ball: Ball):
        ball_bbox = ball.get_ball_bbox()
        for brick in self.bricks:
            brick_bbox = brick.get_brick_bbox()
            if self.ball_hit_top_or_bottom_of_brick(ball_bbox, brick_bbox):
                ball.bounce(HORIZONTAL_SURFACE)
                break
            if self.ball_hit_left_or_right_of_brick(ball_bbox, brick_bbox):
                ball.bounce(VERTICAL_SURFACE)
                break

    @staticmethod
    def ball_hit_top_or_bottom_of_brick(ball_bbox, brick_bbox):
        pass

    @staticmethod
    def ball_hit_left_or_right_of_brick(ball_bbox, brick_bbox):
        pass

    @staticmethod
    def ball_hit_paddle(ball: Ball, paddle_bbox):
        ball_x = ball.xcor()
        ball_bottom_y = ball.ycor() - BALL_RADIUS
        paddle_x1, paddle_y1, paddle_x2 = paddle_bbox[:3]
        return paddle_y1 >= ball_bottom_y >= paddle_y1 - BALL_SPEED and paddle_x1 <= ball_x <= paddle_x2

    @staticmethod
    def ball_missed(ball: Ball):
        return ball.ycor() <= SCREEN_BOTTOM_EDGE + BALL_RADIUS

    @staticmethod
    def ball_hit_top_wall(ball: Ball):
        return ball.ycor() >= SCREEN_TOP_EDGE - BALL_RADIUS

    @staticmethod
    def ball_hit_side_wall(ball: Ball):
        return ball.xcor() >= SCREEN_RIGHT_EDGE - BALL_RADIUS or ball.xcor() <= SCREEN_LEFT_EDGE + BALL_RADIUS
