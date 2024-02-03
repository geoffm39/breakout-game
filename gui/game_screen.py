from tkinter import *
from turtle import TurtleScreen

from paddle import Paddle
from ball import Ball
from bricks import Bricks
from powerup import Powerup
from scores import Scores
from constants import VERTICAL_SURFACE, HORIZONTAL_SURFACE, SCREEN_WIDTH, SCREEN_HEIGHT


class GameScreen(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(background='black')

        self.screen = TurtleScreen(self)
        self.configure_screen()

        self.paddle = Paddle(self.screen)
        self.balls = []

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
            self.check_ball_for_wall_contact(ball)
            if ball.ycor() <= -SCREEN_HEIGHT / 2 + 10:
                return  # THIS IS WHERE GAME END CODE RUNS

        self.after(3, self.update_game_screen)

    def check_ball_for_wall_contact(self, ball):
        if self.ball_hit_side_wall(ball):
            ball.bounce(VERTICAL_SURFACE)
        if self.ball_hit_top_wall(ball):
            ball.bounce(HORIZONTAL_SURFACE)

    @staticmethod
    def ball_hit_top_wall(ball):
        return ball.ycor() >= SCREEN_HEIGHT / 2 - 10

    @staticmethod
    def ball_hit_side_wall(ball):
        return ball.xcor() >= SCREEN_WIDTH / 2 - 10 or ball.xcor() <= -SCREEN_WIDTH / 2 + 10
