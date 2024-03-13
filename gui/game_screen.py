from tkinter import *
from turtle import TurtleScreen
from random import randint, choice

from paddle import Paddle
from ball import Ball
from brick import Brick
from powerup import Powerup
from laser import Laser
from scores import Scores
from levels import Levels
from images.game_images import GameImages
from constants import (
    VERTICAL_SURFACE, HORIZONTAL_SURFACE, BallAttributes, TYPE, SPACING, SPACE_SIZE, BrickAttributes, PowerupAttributes,
    SCREEN_BOTTOM_EDGE, SCREEN_TOP_EDGE, SCREEN_RIGHT_EDGE, SCREEN_LEFT_EDGE, PowerupType, LaserAttributes,
    BrickType, Color, SCREEN_HEIGHT, SCREEN_WIDTH
)


class GameScreen(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(background=Color.BLACK.value)

        self.screen = TurtleScreen(self)
        self.configure_screen()

        self.game_images = GameImages(self)
        self.game_images.apply_background_image()

        self.paddle = None
        self.levels = Levels()
        self.scores = Scores(self.screen)
        self.bricks = []
        self.balls = []
        self.powerups = []
        self.lasers = []

        self.current_level = 1
        self.keyboard_control = True

        self.show_options_screen()

    def show_options_screen(self):
        self.game_images.show_options_screen_images()
        self.scores.show_options_screen_text(self.is_keyboard_controls())

    def handle_keyboard_control_button_press(self):
        self.keyboard_control = True
        self.scores.show_options_screen_text(self.is_keyboard_controls())

    def handle_mouse_control_button_press(self):
        self.keyboard_control = False
        self.scores.show_options_screen_text(self.is_keyboard_controls())

    def is_keyboard_controls(self):
        return self.keyboard_control

    def apply_on_mouse_click_binding(self):
        self.bind('<Button-1>', self.check_for_button_clicks)

    def check_for_button_clicks(self, event):
        yes_button = self.game_images.get_yes_button()
        no_button = self.game_images.get_no_button()
        start_game_button = self.game_images.get_start_game_button()
        keyboard_button = self.game_images.get_keyboard_control_button()
        mouse_button = self.game_images.get_mouse_control_button()
        if yes_button is not None:
            bbox = self.bbox(yes_button)
            if self.mouse_click_on_button((event.x, event.y), bbox):
                self.quit_game()
        if no_button is not None:
            bbox = self.bbox(no_button)
            if self.mouse_click_on_button((event.x, event.y), bbox):
                self.restart_game()
        if start_game_button is not None:
            bbox = self.bbox(start_game_button)
            if self.mouse_click_on_button((event.x, event.y), bbox):
                self.start_game()
                return
        if keyboard_button is not None:
            bbox = self.bbox(keyboard_button)
            if self.mouse_click_on_button((event.x, event.y), bbox):
                self.handle_keyboard_control_button_press()
        if mouse_button is not None:
            bbox = self.bbox(mouse_button)
            if self.mouse_click_on_button((event.x, event.y), bbox):
                self.handle_mouse_control_button_press()
        pass

    @staticmethod
    def mouse_click_on_button(click_location: tuple, button_bbox: tuple):
        x = click_location[0] - SCREEN_WIDTH / 2
        y = click_location[1] - SCREEN_HEIGHT / 2
        return button_bbox[0] < x < button_bbox[2] and button_bbox[1] < y < button_bbox[3]

    def quit_game(self):
        self.quit()

    def restart_game(self):
        self.scores.reset_scores()
        self.game_images.remove_images_on_restart_game()
        self.show_options_screen()

    def track_player_movement(self, event):
        x = event.x
        self.paddle.move_to(x)
        self.game_images.move_object_image(self.paddle)

    def hide_mouse_cursor(self, event=None):
        self.config(cursor='none')

    def show_mouse_cursor(self, event=None):
        self.config(cursor='')

    def configure_screen(self):
        self.screen.tracer(0)
        self.screen.bgcolor(Color.BLACK.value)
        self.screen.listen()
        self.apply_on_mouse_click_binding()

    def start_game(self):
        self.hide_mouse_cursor()
        self.game_images.remove_images_on_start_game()
        self.game_images.apply_lives_image()
        self.paddle = Paddle(self.screen)
        self.game_images.create_object_image(self.paddle)
        self.scores.update_scores()
        self.add_level_bricks()
        self.add_ball()
        if self.keyboard_control:
            self.apply_paddle_keyboard_control()
        else:
            self.apply_paddle_mouse_control()
        self.update_game_screen()

    def apply_paddle_keyboard_control(self):
        self.screen.onkeypress(fun=self.move_paddle_left, key='Left')
        self.screen.onkeypress(fun=self.move_paddle_right, key='Right')

    def apply_paddle_mouse_control(self):
        self.bind('<Motion>', self.track_player_movement)
        self.bind('<Enter>', self.hide_mouse_cursor)
        self.bind('<Leave>', self.show_mouse_cursor)

    def stop_paddle_mouse_control(self):
        self.unbind('<Motion>')
        self.unbind('<Enter>')
        self.unbind('<Leave>')

    def stop_paddle_keyboard_control(self):
        self.screen.onkeypress(fun=None, key='Left')
        self.screen.onkeypress(fun=None, key='Right')

    def update_game_screen(self):
        self.screen.update()
        for ball in self.balls.copy():
            ball.move()
            self.game_images.move_object_image(ball)
            self.check_for_ball_collision(ball)
            if self.ball_missed(ball):
                self.remove_ball(ball)
                if self.no_more_balls():
                    self.scores.decrease_lives()
                    if self.scores.no_more_lives():
                        self.handle_game_over()
                        return
                    else:
                        self.handle_life_lost()
        for powerup in self.powerups.copy():
            powerup.move()
            self.game_images.move_object_image(powerup)
            self.check_for_powerup_collision(powerup)
        for powerup_type_image in self.game_images.get_powerup_type_images():
            self.game_images.move_powerup_type_image(powerup_type_image)
        for laser in self.lasers.copy():
            laser.move()
            self.game_images.move_object_image(laser)
            self.check_for_laser_collision(laser)
        self.after(3, self.update_game_screen)

    def move_paddle_left(self):
        self.paddle.move_left()
        self.game_images.move_object_image(self.paddle)

    def move_paddle_right(self):
        self.paddle.move_right()
        self.game_images.move_object_image(self.paddle)

    def reset_paddle(self):
        self.paddle.reset_size()
        self.paddle.deactivate_lasers()
        self.game_images.update_object_image(self.paddle)

    def fire_paddle_lasers(self):
        paddle_x1, paddle_y1, paddle_x2 = self.paddle.get_bbox()[:3]
        laser_width = LaserAttributes.WIDTH
        laser_y = paddle_y1 + laser_width / 2
        left_laser_x = paddle_x1 + laser_width / 2
        right_laser_x = paddle_x2 - laser_width / 2
        left_laser = Laser(self.screen, (left_laser_x, laser_y))
        self.lasers.append(left_laser)
        self.game_images.create_object_image(left_laser)
        right_laser = Laser(self.screen, (right_laser_x, laser_y))
        self.lasers.append(right_laser)
        self.game_images.create_object_image(right_laser)
        if not self.paddle.is_laser_paddle():
            return
        self.after(LaserAttributes.FREQUENCY, self.fire_paddle_lasers)

    def remove_laser(self, laser: Laser):
        if laser in self.lasers:
            self.game_images.delete_object_image(laser)
            self.lasers.remove(laser)
            del laser

    def check_for_laser_collision(self, laser: Laser):
        self.check_laser_for_brick_collision(laser)
        if self.laser_hit_top_wall(laser):
            self.remove_laser(laser)

    def check_laser_for_brick_collision(self, laser: Laser):
        laser_bbox = laser.get_bbox()
        for brick in self.bricks.copy():
            brick_bbox = brick.get_bbox()
            if self.laser_hit_brick(laser_bbox, brick_bbox):
                brick.hideturtle()
                self.handle_brick_collision(brick)
                self.remove_laser(laser)

    @staticmethod
    def laser_hit_brick(laser_bbox, brick_bbox):
        laser_x = laser_bbox[0] + LaserAttributes.WIDTH / 2
        laser_y1 = laser_bbox[1]
        brick_x1, _, brick_x2, brick_y2 = brick_bbox
        if (brick_x1 - BrickAttributes.SPACING / 2 <= laser_x <= brick_x2 + BrickAttributes.SPACING / 2 and
                brick_y2 <= laser_y1 <= brick_y2 + LaserAttributes.SPEED):
            return True
        return False

    @staticmethod
    def laser_hit_top_wall(laser: Laser):
        return laser.ycor() >= SCREEN_TOP_EDGE - LaserAttributes.WIDTH / 2

    def add_ball(self):
        ball = Ball(self.screen)
        self.balls.append(ball)
        self.game_images.add_ball_animation(ball)

    def add_quicker_ball(self, top_ball_speed):
        quicker_ball = Ball(self.screen)
        quicker_ball.set_speed(top_ball_speed)
        quicker_ball.increase_speed()
        self.balls.append(quicker_ball)
        self.game_images.add_ball_animation(quicker_ball)

    def remove_ball(self, ball: Ball):
        self.game_images.delete_object_image(ball)
        self.balls.remove(ball)
        del ball

    def add_level_bricks(self):
        level_data = self.levels.get_level(self.current_level)
        y_location = SCREEN_TOP_EDGE - BrickAttributes.SPACING
        for row in level_data:
            x_location = SCREEN_LEFT_EDGE + BrickAttributes.SPACING
            for item in row:
                if self.is_spacing(item):
                    x_location += item[SPACE_SIZE]
                    x_location += BrickAttributes.SPACING
                else:
                    new_brick = Brick(self.screen, item)
                    new_brick.set_location(x_location, y_location)
                    self.bricks.append(new_brick)
                    self.game_images.create_object_image(new_brick)
                    x_location += new_brick.get_length()
                    x_location += BrickAttributes.SPACING
            y_location -= BrickAttributes.WIDTH
            y_location -= BrickAttributes.SPACING

    @staticmethod
    def is_spacing(position):
        return position[TYPE] == SPACING

    def check_for_ball_collision(self, ball: Ball):
        self.check_for_paddle_collision(ball)
        self.check_for_brick_collision(ball)
        self.check_for_wall_collision(ball)

    def check_for_wall_collision(self, ball: Ball):
        if self.ball_hit_side_wall(ball):
            ball.bounce(VERTICAL_SURFACE)
            ball.clear_latest_barrier_hit()
        if self.ball_hit_top_wall(ball):
            ball.bounce(HORIZONTAL_SURFACE)
            ball.clear_latest_barrier_hit()

    def check_for_paddle_collision(self, ball: Ball):
        ball_direction = ball.get_direction()
        if ball.is_moving_south_west(ball_direction) or ball.is_moving_south_east(ball_direction):
            if self.ball_hit_paddle(ball):
                paddle_angle_modifier = self.paddle.get_modifier_angle(ball.xcor())
                ball.bounce(HORIZONTAL_SURFACE, paddle_angle_modifier)
                ball.clear_latest_barrier_hit()

    def check_for_brick_collision(self, ball: Ball):
        for brick in self.bricks:
            brick_bbox = brick.get_bbox()
            if self.ball_hit_top_or_bottom_of_brick(ball, brick_bbox):
                self.handle_brick_collision(brick)
                if brick.is_barrier():
                    if self.ball_stuck_inside_brick(ball, brick):
                        break
                    ball.set_latest_barrier_hit(brick)
                    ball.bounce(HORIZONTAL_SURFACE)
                    break
                if ball.is_fireball():
                    ball.clear_latest_barrier_hit()
                    break
                ball.set_latest_barrier_hit(brick)
                ball.bounce(HORIZONTAL_SURFACE)
                break
            elif self.ball_hit_left_or_right_of_brick(ball, brick_bbox):
                self.handle_brick_collision(brick)
                if brick.is_barrier():
                    if self.ball_stuck_inside_brick(ball, brick):
                        break
                    ball.set_latest_barrier_hit(brick)
                    ball.bounce(VERTICAL_SURFACE)
                    break
                if ball.is_fireball():
                    break
                ball.bounce(VERTICAL_SURFACE)
                break

    @staticmethod
    def ball_stuck_inside_brick(ball: Ball, brick: Brick):
        latest_brick = ball.get_latest_barrier_hit()
        return latest_brick == brick

    def check_for_powerup_collision(self, powerup: Powerup):
        if self.powerup_hit_paddle(powerup):
            self.activate_powerup(powerup)
            self.remove_powerup(powerup)
        if self.powerup_missed(powerup):
            self.remove_powerup(powerup)

    def ball_hit_paddle(self, ball: Ball):
        ball_x = ball.xcor()
        ball_bottom_y = ball.ycor() - BallAttributes.RADIUS
        paddle_x1, paddle_y1, paddle_x2 = self.paddle.get_bbox()[:3]
        return paddle_y1 >= ball_bottom_y >= paddle_y1 - ball.get_speed() and paddle_x1 <= ball_x <= paddle_x2

    @staticmethod
    def ball_missed(ball: Ball):
        return ball.ycor() <= SCREEN_BOTTOM_EDGE + BallAttributes.RADIUS

    @staticmethod
    def ball_hit_top_wall(ball: Ball):
        return ball.ycor() >= SCREEN_TOP_EDGE - BallAttributes.RADIUS

    @staticmethod
    def ball_hit_side_wall(ball: Ball):
        ball_radius = BallAttributes.RADIUS
        return ball.xcor() >= SCREEN_RIGHT_EDGE - ball_radius or ball.xcor() <= SCREEN_LEFT_EDGE + ball_radius

    def no_more_balls(self):
        return len(self.balls) == 0

    @staticmethod
    def ball_hit_top_or_bottom_of_brick(ball: Ball, brick_bbox):
        ball_x1, ball_y1, _, ball_y2 = ball.get_bbox()
        ball_x = ball_x1 + BallAttributes.RADIUS
        brick_x1, brick_y1, brick_x2, brick_y2 = brick_bbox
        if brick_x1 - BrickAttributes.SPACING / 2 <= ball_x <= brick_x2 + BrickAttributes.SPACING / 2:
            if brick_y1 >= ball_y2 >= brick_y1 - ball.get_speed():
                return True
            if brick_y2 <= ball_y1 <= brick_y2 + ball.get_speed():
                return True
        return False

    @staticmethod
    def ball_hit_left_or_right_of_brick(ball: Ball, brick_bbox):
        ball_x1, ball_y1, ball_x2, _ = ball.get_bbox()
        ball_y = ball_y1 - BallAttributes.RADIUS
        brick_x1, brick_y1, brick_x2, brick_y2 = brick_bbox
        if brick_y1 + BrickAttributes.SPACING / 2 >= ball_y >= brick_y2 - BrickAttributes.SPACING / 2:
            if brick_x1 <= ball_x2 <= brick_x1 + ball.get_speed():
                return True
            if brick_x2 >= ball_x1 >= brick_x2 - ball.get_speed():
                return True
        return False

    def handle_brick_collision(self, brick: Brick):
        if brick.is_normal() or brick.is_broken():
            self.scores.increase_score(brick.get_score())
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
        if self.current_level > self.levels.get_number_of_levels():
            self.current_level = 1
        top_ball_speed = self.get_quickest_ball_speed()
        self.reset_game_screen()
        self.add_level_bricks()
        self.add_quicker_ball(top_ball_speed)

    def reset_game_screen(self):
        for brick in self.bricks.copy():
            self.remove_brick(brick)
        for ball in self.balls.copy():
            self.remove_ball(ball)
        for powerup in self.powerups.copy():
            self.remove_powerup(powerup)
        for laser in self.lasers.copy():
            self.remove_laser(laser)
        self.reset_paddle()

    def handle_game_over(self):
        self.reset_game_screen()
        self.game_images.handle_game_over_images(self.paddle)
        self.scores.check_for_highscore()
        self.stop_paddle_mouse_control()
        self.stop_paddle_keyboard_control()
        self.show_mouse_cursor()

    def handle_life_lost(self):
        for powerup in self.powerups.copy():
            self.remove_powerup(powerup)
        self.reset_paddle()
        self.add_ball()

    def get_quickest_ball_speed(self):
        top_speed = 0
        for ball in self.balls:
            speed = ball.get_speed()
            if speed > top_speed:
                top_speed = speed
        return top_speed

    def handle_strong_brick_collision(self, brick: Brick):
        brick.set_type(BrickType.BROKEN)
        self.game_images.update_object_image(brick)

    def remove_brick(self, brick: Brick):
        self.check_powerup_drop(brick)
        self.game_images.delete_object_image(brick)
        self.bricks.remove(brick)
        del brick

    def check_powerup_drop(self, brick):
        if self.brick_has_powerup(brick):
            self.drop_powerup(brick)

    @staticmethod
    def brick_has_powerup(brick: Brick):
        if not brick.is_barrier():
            return randint(1, 6) == 1
        return False

    def drop_powerup(self, brick: Brick):
        random_powerup_type = choice(list(PowerupType))
        location = brick.get_location()
        self.add_powerup(random_powerup_type, location)

    def add_powerup(self, powerup_type, location):
        new_powerup = Powerup(self.screen, powerup_type, location)
        self.powerups.append(new_powerup)
        self.game_images.create_object_image(new_powerup)

    def remove_powerup(self, powerup: Powerup):
        self.game_images.delete_object_image(powerup)
        self.powerups.remove(powerup)
        del powerup

    def powerup_hit_paddle(self, powerup: Powerup):
        powerup_x = powerup.xcor()
        powerup_bottom_y = powerup.ycor() - PowerupAttributes.WIDTH / 2
        paddle_x1, paddle_y1, paddle_x2 = self.paddle.get_bbox()[:3]
        return (paddle_y1 >= powerup_bottom_y >= paddle_y1 - PowerupAttributes.SPEED and
                paddle_x1 <= powerup_x <= paddle_x2)

    @staticmethod
    def powerup_missed(powerup: Powerup):
        return powerup.ycor() <= SCREEN_BOTTOM_EDGE + PowerupAttributes.WIDTH / 2

    def activate_powerup(self, powerup: Powerup):
        powerup_type = powerup.get_type()
        powerup_actions = {
            PowerupType.MULTIBALL: self.activate_multiball,
            PowerupType.FIREBALL: self.activate_fireball,
            PowerupType.SLOW_BALL: self.activate_slow_ball,
            PowerupType.FAST_BALL: self.activate_fast_ball,
            PowerupType.LASERS: self.activate_lasers,
            PowerupType.SMALL_PADDLE: self.activate_small_paddle,
            PowerupType.BIG_PADDLE: self.activate_big_paddle,
            PowerupType.EXTRA_LIFE: self.activate_extra_life
        }
        if powerup_type in powerup_actions:
            powerup_actions[powerup_type]()
            self.game_images.add_powerup_type_image(powerup_type, self.paddle)

    def move_powerup_type_image(self, canvas_image):
        if canvas_image:
            self.move(canvas_image, 0, PowerupAttributes.IMAGE_SPEED)

    def activate_multiball(self):
        self.add_ball()

    def activate_fireball(self):
        for ball in self.balls:
            ball.activate_fireball()
            self.game_images.update_object_image(ball)

    def activate_slow_ball(self):
        for ball in self.balls:
            ball.decrease_speed()

    def activate_fast_ball(self):
        for ball in self.balls:
            ball.increase_speed()

    def activate_lasers(self):
        self.paddle.activate_lasers()
        self.game_images.update_object_image(self.paddle)
        self.fire_paddle_lasers()
        self.after(LaserAttributes.TIME_LIMIT, self.deactivate_lasers)

    def deactivate_lasers(self):
        self.paddle.deactivate_lasers()
        self.game_images.update_object_image(self.paddle)

    def activate_small_paddle(self):
        self.paddle.decrease_size()
        self.game_images.update_object_image(self.paddle)

    def activate_big_paddle(self):
        self.paddle.increase_size()
        self.game_images.update_object_image(self.paddle)

    def activate_extra_life(self):
        self.scores.increase_lives()
