from turtle import Screen

from paddle import Paddle
from ball import Ball
from brick import Brick
from powerup import Powerup
from scores import Scores
from levels import Levels
from constants import (
    VERTICAL_SURFACE, HORIZONTAL_SURFACE, BALL_RADIUS, BRICK_SPACING, TYPE, SPACING, SPACE_SIZE,
    BRICK_LOCATION, BARRIER, BARRIER_LENGTH, BRICK_WIDTH, BRICK_LENGTH, SCREEN_WIDTH, SCREEN_HEIGHT,
    SCREEN_BOTTOM_EDGE, SCREEN_TOP_EDGE, SCREEN_RIGHT_EDGE, SCREEN_LEFT_EDGE
)


class GameScreen:
    def __init__(self):
        self.screen = Screen()

        self.paddle = Paddle()
        self.levels = Levels()
        self.bricks = []
        self.balls = []

    def setup_screen(self):
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.screen.tracer(0)
        self.screen.bgcolor('black')
        self.screen.title('Breakout!')
        self.screen.listen()

    def run(self):
        self.screen.mainloop()

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
                    new_brick = Brick(self, item)
                    new_brick.set_brick_location(x_location, y_location)
                    self.bricks.append(new_brick)
                    x_location += new_brick.get_brick_length()
                    x_location += BRICK_SPACING
            y_location -= BRICK_WIDTH
            y_location -= BRICK_SPACING


if __name__ == '__main__':
    screen = GameScreen()
    screen.setup_screen()
    screen.run()
