from tkinter import *
from turtle import TurtleScreen, RawTurtle

from paddle import Paddle
from ball import Ball
from brick import Brick
from powerup import Powerup
from scores import Scores
from levels import Levels
from images.game_images import GameImages
from constants import (
    VERTICAL_SURFACE, HORIZONTAL_SURFACE, BALL_RADIUS, BRICK_SPACING, TYPE, SPACING, SPACE_SIZE, BRICK_WIDTH,
    SCREEN_BOTTOM_EDGE, SCREEN_TOP_EDGE, SCREEN_RIGHT_EDGE, SCREEN_LEFT_EDGE, BALL_SPEED, BROKEN, SCREEN_WIDTH
)


class GameScreen(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(background='black')

        self.screen = TurtleScreen(self)
        self.configure_screen()

        self.game_images = GameImages()

        self.paddle = Paddle(self.screen)
        self.levels = Levels()
        self.bricks = []
        self.brick_images = []
        self.balls = []

        self.current_level = 1

        self.apply_mouse_controls()
        self.apply_background_image()

    def apply_mouse_controls(self):
        self.bind('<Motion>', self.track_player_movement)
        self.bind('<Enter>', self.hide_mouse_cursor)
        self.bind('<Leave>', self.show_mouse_cursor)

    def apply_background_image(self):
        background = self.game_images.get_background()
        self.create_image(0, 0, image=background)

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
                    new_brick.set_location(x_location, y_location)
                    self.bricks.append(new_brick)
                    self.add_brick_image(new_brick)
                    x_location += new_brick.get_length()
                    x_location += BRICK_SPACING
            y_location -= BRICK_WIDTH
            y_location -= BRICK_SPACING

    def add_brick_image(self, brick):
        image = self.game_images.get_brick_image(brick)
        screen_x, screen_y = brick.get_location()
        canvas_x = screen_x
        canvas_y = screen_y * -1
        canvas_image = self.create_image(canvas_x, canvas_y, image=image)
        self.brick_images.append(canvas_image)

    @staticmethod
    def is_spacing(position):
        return position[TYPE] == SPACING

    def update_game_screen(self):
        self.screen.update()
        for ball in self.balls:
            ball.move()
            self.check_for_ball_collision(ball)
            if self.ball_missed(ball):
                return
        self.after(3, self.update_game_screen)

    def check_for_ball_collision(self, ball: Ball):
        self.check_for_paddle_collision(ball)
        self.check_for_brick_collision(ball)
        self.check_for_wall_collision(ball)

    def check_for_wall_collision(self, ball: Ball):
        if self.ball_hit_side_wall(ball):
            ball.bounce(VERTICAL_SURFACE)
        if self.ball_hit_top_wall(ball):
            ball.bounce(HORIZONTAL_SURFACE)

    def check_for_paddle_collision(self, ball: Ball):
        ball_direction = ball.get_direction()
        if ball.is_moving_south_west(ball_direction) or ball.is_moving_south_east(ball_direction):
            paddle_bbox = self.paddle.get_bbox()
            if self.ball_hit_paddle(ball, paddle_bbox):
                paddle_angle_modifier = self.paddle.get_modifier_angle(ball.xcor())
                ball.bounce(HORIZONTAL_SURFACE, paddle_angle_modifier)

    def check_for_brick_collision(self, ball: Ball):
        ball_bbox = ball.get_bbox()
        for brick in self.bricks:
            brick_bbox = brick.get_bbox()
            if self.ball_hit_top_or_bottom_of_brick(ball_bbox, brick_bbox):
                brick.hideturtle()
                self.handle_brick_collision(brick)
                ball.bounce(HORIZONTAL_SURFACE)
                break
            if self.ball_hit_left_or_right_of_brick(ball_bbox, brick_bbox):
                brick.hideturtle()
                self.handle_brick_collision(brick)
                ball.bounce(VERTICAL_SURFACE)
                break

    @staticmethod
    def ball_hit_top_or_bottom_of_brick(ball_bbox, brick_bbox):
        ball_x = ball_bbox[0] + BALL_RADIUS
        ball_y1, ball_y2 = ball_bbox[1::2]
        brick_x1, brick_y1, brick_x2, brick_y2 = brick_bbox
        if brick_x1 - BRICK_SPACING / 2 <= ball_x <= brick_x2 + BRICK_SPACING / 2:
            if brick_y1 >= ball_y2 >= brick_y1 - BALL_SPEED:
                return True
            if brick_y2 <= ball_y1 <= brick_y2 + BALL_SPEED:
                return True
        return False

    @staticmethod
    def ball_hit_left_or_right_of_brick(ball_bbox, brick_bbox):
        ball_y = ball_bbox[1] - BALL_RADIUS
        ball_x1, ball_x2 = ball_bbox[::2]
        brick_x1, brick_y1, brick_x2, brick_y2 = brick_bbox
        if brick_y1 + BRICK_SPACING / 2 >= ball_y >= brick_y2 - BRICK_SPACING / 2:
            if brick_x1 <= ball_x2 <= brick_x1 + BALL_SPEED:
                return True
            if brick_x2 >= ball_x1 >= brick_x2 - BALL_SPEED:
                return True
        return False

    def handle_brick_collision(self, brick):
        if brick.is_normal() or brick.is_broken():
            self.remove_brick(brick)
        elif brick.is_strong():
            self.handle_strong_brick_collision(brick)
        if self.level_is_complete():
            self.progress_to_next_level()

    def level_is_complete(self):
        if len(self.bricks) == 0:
            return True
        for brick in self.bricks:
            if not brick.is_barrier():
                return False
        return True

    def progress_to_next_level(self):
        self.current_level += 1
        for brick in self.bricks:
            self.remove_brick(brick)
        for ball in self.balls:
            self.remove_ball(ball)
        self.add_level_bricks()
        self.balls.append(Ball(self.screen))

    def handle_strong_brick_collision(self, brick):
        brick_index = self.bricks.index(brick)
        brick.set_type(BROKEN)
        updated_image = self.game_images.get_brick_image(brick)
        self.itemconfig(self.brick_images[brick_index], image=updated_image)

    def remove_brick(self, brick):
        brick_index = self.bricks.index(brick)
        self.delete(self.brick_images[brick_index])
        self.brick_images.pop(brick_index)
        self.bricks.remove(brick)

    def remove_ball(self, ball):
        ball.remove_ball()
        self.balls.remove(ball)

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
