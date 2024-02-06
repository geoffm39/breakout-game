from tkinter import *
from turtle import TurtleScreen

from paddle import Paddle
from ball import Ball
from brick import Brick
from powerup import Powerup
from scores import Scores
from constants import (
    VERTICAL_SURFACE, HORIZONTAL_SURFACE, BALL_RADIUS,
    SCREEN_BOTTOM_EDGE, SCREEN_TOP_EDGE, SCREEN_RIGHT_EDGE, SCREEN_LEFT_EDGE
)


class GameScreen(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(background='black')

        self.screen = TurtleScreen(self)
        self.configure_screen()

        self.paddle = Paddle(self.screen)
        self.balls = []
        self.bricks = []

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
        self.balls.append(Ball(self.screen))
        self.update_game_screen()

    def update_game_screen(self):
        self.screen.update()
        for ball in self.balls:
            ball.move()
            self.check_for_paddle_contact(ball)
            self.check_for_wall_contact(ball)
            if self.ball_missed(ball):
                return
        self.after(3, self.update_game_screen)

    def check_for_wall_contact(self, ball):
        if self.ball_hit_side_wall(ball):
            ball.bounce(VERTICAL_SURFACE)
        if self.ball_hit_top_wall(ball):
            ball.bounce(HORIZONTAL_SURFACE)

    def check_for_paddle_contact(self, ball):
        paddle_bbox = self.paddle.get_paddle_bbox()
        if self.ball_hit_paddle(ball, paddle_bbox):
            paddle_angle_modifier = self.paddle.get_paddle_modifier_angle(ball.xcor())
            ball.bounce(HORIZONTAL_SURFACE, paddle_angle_modifier)

    @staticmethod
    def ball_hit_paddle(ball, paddle_bbox):
        ball_x, ball_y = ball.pos()
        ball_bottom_y = int(ball_y - BALL_RADIUS)
        paddle_x1, paddle_y1, paddle_x2 = paddle_bbox[:3]
        return ball_bottom_y == paddle_y1 and paddle_x1 <= ball_x <= paddle_x2

    @staticmethod
    def ball_missed(ball):
        return ball.ycor() <= SCREEN_BOTTOM_EDGE + BALL_RADIUS

    @staticmethod
    def ball_hit_top_wall(ball):
        return ball.ycor() >= SCREEN_TOP_EDGE - BALL_RADIUS

    @staticmethod
    def ball_hit_side_wall(ball):
        return ball.xcor() >= SCREEN_RIGHT_EDGE - BALL_RADIUS or ball.xcor() <= SCREEN_LEFT_EDGE + BALL_RADIUS
