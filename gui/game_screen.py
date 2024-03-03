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
    VERTICAL_SURFACE, HORIZONTAL_SURFACE, BALL_RADIUS, BRICK_SPACING, TYPE, SPACING, SPACE_SIZE, BRICK_WIDTH,
    SCREEN_BOTTOM_EDGE, SCREEN_TOP_EDGE, SCREEN_RIGHT_EDGE, SCREEN_LEFT_EDGE, PowerupType,
    POWERUP_WIDTH, POWERUP_SPEED, LASER_WIDTH, LASER_SPEED, LASER_TIME_LIMIT, LASER_FREQUENCY, SCREEN_HEIGHT,
    POWERUP_IMAGE_TIME_LIMIT, POWERUP_IMAGE_SPEED, BALL_ANIMATION_SPEED,
    BrickType, LIVES_IMAGE_X_COORD, LIVES_IMAGE_Y_COORD
)


class GameScreen(Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(background='black')

        self.screen = TurtleScreen(self)
        self.configure_screen()

        self.game_images = GameImages()
        self.apply_background_image()
        self.apply_lives_image()

        self.paddle = Paddle(self.screen)
        self.paddle_canvas_image = None
        self.levels = Levels()
        self.scores = Scores(self.screen)
        self.bricks = []
        self.brick_images = []
        self.balls = []
        self.ball_animations = []
        self.powerups = []
        self.powerup_images = []
        self.powerup_type_images = []
        self.lasers = []
        self.laser_images = []

        self.latest_collision_brick = None

        self.current_level = 1

        self.apply_mouse_controls()

        self.set_paddle_image()

    def apply_mouse_controls(self):
        self.bind('<Motion>', self.track_player_movement)
        self.bind('<Enter>', self.hide_mouse_cursor)
        self.bind('<Leave>', self.show_mouse_cursor)

    def apply_background_image(self):
        background = self.game_images.get_background()
        self.create_image(0, 0, image=background)

    def apply_lives_image(self):
        lives = self.game_images.get_lives()
        self.create_image(LIVES_IMAGE_X_COORD, LIVES_IMAGE_Y_COORD, image=lives)

    def set_paddle_image(self):
        image = self.game_images.get_paddle(self.paddle)
        screen_x, screen_y = self.paddle.get_location()
        canvas_x = screen_x
        canvas_y = screen_y * -1
        self.paddle_canvas_image = self.create_image(canvas_x, canvas_y, image=image)

    def move_paddle_image(self):
        paddle_x, paddle_y = self.paddle.get_location()
        self.coords(self.paddle_canvas_image, (paddle_x, paddle_y * -1))

    def update_paddle_image(self):
        updated_image = self.game_images.get_paddle(self.paddle)
        self.itemconfig(self.paddle_canvas_image, image=updated_image)

    def reset_paddle(self):
        self.paddle.reset_size()
        image = self.game_images.get_paddle(self.paddle)
        self.itemconfig(self.paddle_canvas_image, image=image)

    def fire_paddle_lasers(self):
        paddle_x1, paddle_y1, paddle_x2 = self.paddle.get_bbox()[:3]
        laser_y = paddle_y1 + LASER_WIDTH / 2
        left_laser_x = paddle_x1 + LASER_WIDTH / 2
        right_laser_x = paddle_x2 - LASER_WIDTH / 2
        left_laser = Laser(self.screen, (left_laser_x, laser_y))
        self.lasers.append(left_laser)
        self.add_laser_image(left_laser)
        right_laser = Laser(self.screen, (right_laser_x, laser_y))
        self.lasers.append(right_laser)
        self.add_laser_image(right_laser)
        if not self.paddle.is_laser_paddle():
            return
        self.after(LASER_FREQUENCY, self.fire_paddle_lasers)

    def add_laser_image(self, laser: Laser):
        image = self.game_images.get_laser()
        screen_x, screen_y = laser.get_location()
        canvas_x = screen_x
        canvas_y = screen_y * -1
        canvas_image = self.create_image(canvas_x, canvas_y, image=image)
        self.laser_images.append(canvas_image)

    def remove_laser(self, laser: Laser):
        if laser in self.lasers:
            laser_index = self.lasers.index(laser)
            self.delete(self.laser_images[laser_index])
            self.laser_images.pop(laser_index)
            self.lasers.remove(laser)
            del laser

    def move_laser_image(self, laser: Laser):
        laser_index = self.lasers.index(laser)
        self.move(self.laser_images[laser_index], 0, LASER_SPEED * -1)

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
        laser_x = laser_bbox[0] + LASER_WIDTH / 2
        laser_y1 = laser_bbox[1]
        brick_x1, _, brick_x2, brick_y2 = brick_bbox
        if (brick_x1 - BRICK_SPACING / 2 <= laser_x <= brick_x2 + BRICK_SPACING / 2 and
                brick_y2 <= laser_y1 <= brick_y2 + LASER_SPEED):
            return True
        return False

    @staticmethod
    def laser_hit_top_wall(laser: Laser):
        return laser.ycor() >= SCREEN_TOP_EDGE - LASER_WIDTH / 2

    def track_player_movement(self, event):
        x = event.x
        self.paddle.move_to(x)
        self.move_paddle_image()

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
        self.add_ball()
        self.update_game_screen()

    def add_ball(self):
        ball = Ball(self.screen)
        self.balls.append(ball)
        self.add_ball_animation(ball)

    def add_quicker_ball(self, top_ball_speed):
        quicker_ball = Ball(self.screen)
        quicker_ball.set_speed(top_ball_speed)
        quicker_ball.increase_speed()
        self.balls.append(quicker_ball)
        self.add_ball_animation(quicker_ball)

    def add_ball_animation(self, ball: Ball):
        if ball.is_fireball():
            frame = self.game_images.get_fireball_frame()
        else:
            frame = self.game_images.get_ball_frame()
        screen_x, screen_y = ball.get_location()
        canvas_x = screen_x
        canvas_y = screen_y * -1
        canvas_image = self.create_image(canvas_x, canvas_y, image=frame)
        self.ball_animations.append(canvas_image)
        self.cycle_ball_animation_frames(ball, 0)

    def set_fireball_animation(self, ball: Ball):
        ball_index = self.balls.index(ball)
        self.itemconfig(self.ball_animations[ball_index], image=self.game_images.get_fireball_frame())

    def cycle_ball_animation_frames(self, ball: Ball, frame_index):
        if ball in self.balls:
            frame_index = (frame_index + 1) % self.game_images.get_number_of_fireball_frames()
            ball_index = self.balls.index(ball)
            if ball.is_fireball():
                frame = self.game_images.get_fireball_frame(frame_index)
            else:
                frame = self.game_images.get_ball_frame(frame_index)
            self.itemconfig(self.ball_animations[ball_index], image=frame)
            self.after(BALL_ANIMATION_SPEED, self.cycle_ball_animation_frames, ball, frame_index)

    def move_ball_animation(self, ball: Ball):
        if ball in self.balls:
            ball_x, ball_y = ball.get_location()
            ball_index = self.balls.index(ball)
            self.coords(self.ball_animations[ball_index], (ball_x, ball_y * -1))

    def remove_ball(self, ball: Ball):
        ball_index = self.balls.index(ball)
        self.delete(self.ball_animations[ball_index])
        self.balls.remove(ball)
        self.ball_animations.pop(ball_index)
        del ball

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

    def add_brick_image(self, brick: Brick):
        image = self.game_images.get_brick(brick)
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
        for ball in self.balls.copy():
            ball.move()
            self.move_ball_animation(ball)
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
            self.move_powerup_image(powerup)
            self.check_for_powerup_collision(powerup)
        for powerup_type_image in self.powerup_type_images:
            self.move_powerup_type_image(powerup_type_image)
        for laser in self.lasers.copy():
            laser.move()
            self.move_laser_image(laser)
            self.check_for_laser_collision(laser)
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
            if self.ball_hit_paddle(ball):
                paddle_angle_modifier = self.paddle.get_modifier_angle(ball.xcor())
                ball.bounce(HORIZONTAL_SURFACE, paddle_angle_modifier)

    def check_for_brick_collision(self, ball: Ball):
        for brick in self.bricks.copy():
            brick_bbox = brick.get_bbox()
            if self.ball_hit_top_or_bottom_of_brick(ball, brick_bbox):
                self.handle_brick_collision(brick)
                if brick.is_barrier():
                    if self.brick_is_latest_collision_brick(brick):
                        self.set_latest_collision_brick(None)
                        break
                    ball.bounce(HORIZONTAL_SURFACE)
                    self.set_latest_collision_brick(brick)
                    break
                if ball.is_fireball():
                    break
                ball.bounce(HORIZONTAL_SURFACE)
                break
            if self.ball_hit_left_or_right_of_brick(ball, brick_bbox):
                self.handle_brick_collision(brick)
                if brick.is_barrier():
                    if self.brick_is_latest_collision_brick(brick):
                        self.set_latest_collision_brick(None)
                        break
                    ball.bounce(VERTICAL_SURFACE)
                    self.set_latest_collision_brick(brick)
                    break
                if ball.is_fireball():
                    break
                ball.bounce(VERTICAL_SURFACE)
                break

    def set_latest_collision_brick(self, brick):
        self.latest_collision_brick = brick

    def brick_is_latest_collision_brick(self, brick):
        return brick == self.latest_collision_brick

    def check_for_powerup_collision(self, powerup: Powerup):
        if self.powerup_hit_paddle(powerup):
            self.activate_powerup(powerup)
            self.remove_powerup(powerup)
        if self.powerup_missed(powerup):
            self.remove_powerup(powerup)

    def ball_hit_paddle(self, ball: Ball):
        ball_x = ball.xcor()
        ball_bottom_y = ball.ycor() - BALL_RADIUS
        paddle_x1, paddle_y1, paddle_x2 = self.paddle.get_bbox()[:3]
        return paddle_y1 >= ball_bottom_y >= paddle_y1 - ball.get_speed() and paddle_x1 <= ball_x <= paddle_x2

    @staticmethod
    def ball_missed(ball: Ball):
        return ball.ycor() <= SCREEN_BOTTOM_EDGE + BALL_RADIUS

    @staticmethod
    def ball_hit_top_wall(ball: Ball):
        return ball.ycor() >= SCREEN_TOP_EDGE - BALL_RADIUS

    @staticmethod
    def ball_hit_side_wall(ball: Ball):
        return ball.xcor() >= SCREEN_RIGHT_EDGE - BALL_RADIUS or ball.xcor() <= SCREEN_LEFT_EDGE + BALL_RADIUS

    def no_more_balls(self):
        return len(self.balls) == 0

    # @staticmethod
    # def ball_is_inside_brick(ball: Ball, brick_bbox):
    #     ball_x, ball_y = ball.get_location()
    #     brick_x1, brick_y1, brick_x2, brick_y2 = brick_bbox
    #     ball_speed = ball.get_speed()
    #     if brick_x1 + ball_speed <= ball_x <= brick_x2 - ball_speed:
    #         if brick_y1 - ball_speed >= ball_y >= brick_y2 + ball_speed:
    #             return True
    #     return False

    @staticmethod
    def ball_hit_top_or_bottom_of_brick(ball: Ball, brick_bbox):
        ball_x1, ball_y1, _, ball_y2 = ball.get_bbox()
        ball_x = ball_x1 + BALL_RADIUS
        brick_x1, brick_y1, brick_x2, brick_y2 = brick_bbox
        if brick_x1 - BRICK_SPACING / 2 <= ball_x <= brick_x2 + BRICK_SPACING / 2:
            if brick_y1 >= ball_y2 >= brick_y1 - ball.get_speed():
                return True
            if brick_y2 <= ball_y1 <= brick_y2 + ball.get_speed():
                return True
        return False

    @staticmethod
    def ball_hit_left_or_right_of_brick(ball: Ball, brick_bbox):
        ball_x1, ball_y1, ball_x2, _ = ball.get_bbox()
        ball_y = ball_y1 - BALL_RADIUS
        brick_x1, brick_y1, brick_x2, brick_y2 = brick_bbox
        if brick_y1 + BRICK_SPACING / 2 >= ball_y >= brick_y2 - BRICK_SPACING / 2:
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
        for brick in self.bricks.copy():
            self.remove_brick(brick)
        for ball in self.balls.copy():
            self.remove_ball(ball)
        for powerup in self.powerups.copy():
            self.remove_powerup(powerup)
        self.reset_paddle()
        self.add_level_bricks()
        self.add_quicker_ball(top_ball_speed)

    def handle_game_over(self):
        self.scores.check_for_highscore()

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
        brick_index = self.bricks.index(brick)
        brick.set_type(BrickType.BROKEN)
        updated_image = self.game_images.get_brick(brick)
        self.itemconfig(self.brick_images[brick_index], image=updated_image)

    def remove_brick(self, brick: Brick):
        brick.hideturtle()
        self.check_powerup_drop(brick)
        brick_index = self.bricks.index(brick)
        self.delete(self.brick_images[brick_index])
        self.brick_images.pop(brick_index)
        self.bricks.remove(brick)
        del brick

    def check_powerup_drop(self, brick):
        if self.brick_has_powerup(brick):
            self.drop_powerup(brick)

    @staticmethod
    def brick_has_powerup(brick: Brick):
        if not brick.is_barrier():
            return randint(1, 1) == 1
        return False

    def drop_powerup(self, brick: Brick):
        random_powerup_type = choice(list(PowerupType))
        location = brick.get_location()
        self.add_powerup(random_powerup_type, location)

    def add_powerup(self, powerup_type, location):
        new_powerup = Powerup(self.screen, powerup_type, location)
        self.powerups.append(new_powerup)
        self.add_powerup_image(new_powerup)

    def add_powerup_image(self, powerup: Powerup):
        image = self.game_images.get_powerup()
        screen_x, screen_y = powerup.get_location()
        canvas_x = screen_x
        canvas_y = screen_y * -1
        canvas_image = self.create_image(canvas_x, canvas_y, image=image)
        self.powerup_images.append(canvas_image)

    def remove_powerup(self, powerup: Powerup):
        powerup_index = self.powerups.index(powerup)
        self.delete(self.powerup_images[powerup_index])
        self.powerup_images.pop(powerup_index)
        self.powerups.remove(powerup)
        del powerup

    def move_powerup_image(self, powerup: Powerup):
        powerup_index = self.powerups.index(powerup)
        self.move(self.powerup_images[powerup_index], 0, POWERUP_SPEED)

    def powerup_hit_paddle(self, powerup: Powerup):
        powerup_x = powerup.xcor()
        powerup_bottom_y = powerup.ycor() - POWERUP_WIDTH / 2
        paddle_x1, paddle_y1, paddle_x2 = self.paddle.get_bbox()[:3]
        return paddle_y1 >= powerup_bottom_y >= paddle_y1 - POWERUP_SPEED and paddle_x1 <= powerup_x <= paddle_x2

    @staticmethod
    def powerup_missed(powerup: Powerup):
        return powerup.ycor() <= SCREEN_BOTTOM_EDGE + POWERUP_WIDTH / 2

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
            self.add_powerup_type_image(powerup_type)

    def add_powerup_type_image(self, powerup_type: PowerupType):
        image = self.game_images.get_powerup_type(powerup_type)
        canvas_x = self.paddle.xcor()
        canvas_y = SCREEN_HEIGHT / 2 - 50
        canvas_image = self.create_image(canvas_x, canvas_y, image=image)
        self.powerup_type_images.append(canvas_image)
        self.after(POWERUP_IMAGE_TIME_LIMIT, lambda: self.remove_powerup_type_image(canvas_image))

    def move_powerup_type_image(self, canvas_image):
        if canvas_image:
            self.move(canvas_image, 0, POWERUP_IMAGE_SPEED)

    def remove_powerup_type_image(self, canvas_image):
        self.delete(canvas_image)
        self.powerup_type_images.remove(canvas_image)

    def activate_multiball(self):
        self.add_ball()

    def activate_fireball(self):
        for ball in self.balls:
            ball.activate_fireball()
            self.set_fireball_animation(ball)

    def activate_slow_ball(self):
        for ball in self.balls:
            ball.decrease_speed()

    def activate_fast_ball(self):
        for ball in self.balls:
            ball.increase_speed()

    def activate_lasers(self):
        self.paddle.activate_lasers()
        self.update_paddle_image()
        self.fire_paddle_lasers()
        self.after(LASER_TIME_LIMIT, self.deactivate_lasers)

    def deactivate_lasers(self):
        self.paddle.deactivate_lasers()
        self.update_paddle_image()

    def activate_small_paddle(self):
        self.paddle.decrease_size()
        self.update_paddle_image()

    def activate_big_paddle(self):
        self.paddle.increase_size()
        self.update_paddle_image()

    def activate_extra_life(self):
        self.scores.increase_lives()
