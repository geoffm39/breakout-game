from enum import Enum


IMAGE_DIRECTORY = 'images/image-files'
BACKGROUND_FILENAME = 'background.jpg'
POWERUP_FILENAME = 'powerup.png'
PADDLE_FILENAME = 'paddle.png'
PADDLE_LASERS_FILENAME = 'paddle-lasers.png'
LASER_FILENAME = 'laser.png'
FIREBALL_FILENAME = 'fireball.gif'
BALL_FILENAME = 'ball.gif'
LIVES_FILENAME = 'lives.png'
HIGHSCORE_FILENAME = 'highscore.txt'

SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1080

SCREEN_LEFT_EDGE = -SCREEN_WIDTH / 2
SCREEN_RIGHT_EDGE = SCREEN_WIDTH / 2
SCREEN_TOP_EDGE = SCREEN_HEIGHT / 2 - 50
SCREEN_BOTTOM_EDGE = -SCREEN_HEIGHT / 2

LIVES_POSITION = (SCREEN_RIGHT_EDGE - 50, SCREEN_HEIGHT / 2 - 50)
LIVES_IMAGE_X_COORD = SCREEN_RIGHT_EDGE - 105
LIVES_IMAGE_Y_COORD = (SCREEN_TOP_EDGE + 26) * -1
SCORE_POSITION = (0, SCREEN_HEIGHT / 2 - 50)
HIGHSCORE_POSITION = (SCREEN_LEFT_EDGE + 50, SCREEN_HEIGHT / 2 - 50)
GAME_FONT = ('Courier', 32, 'bold')

STARTING_LIVES = 3
MAX_LIVES = 5

SPACING = 'spacing'
SPACE_SIZE = 'space_size'
TYPE = 'type'
BRICK_COLOR = 'brick_color'
VERTICAL_SURFACE = 'vertical'
HORIZONTAL_SURFACE = 'horizontal'

EAST = 0
NORTH = 90
WEST = 180
SOUTH = 270
COMPLETE_ANGLE = 360


class Color(Enum):
    BLUE = 'blue'
    RED = 'red'
    YELLOW = 'yellow'
    ORANGE = 'orange'
    GREEN = 'green'
    PURPLE = 'purple'
    WHITE = 'white'


class Shape(Enum):
    SQUARE = 'square'
    CIRCLE = 'circle'
    ARROW = 'arrow'


class BrickType(Enum):
    NORMAL = 'normal'
    STRONG = 'strong'
    BROKEN = 'broken'
    BARRIER = 'barrier'


class PowerupType(Enum):
    MULTIBALL = 'multiball'
    FIREBALL = 'fireball'
    SLOW_BALL = 'slow_ball'
    FAST_BALL = 'fast_ball'
    LASERS = 'lasers'
    SMALL_PADDLE = 'small_paddle'
    BIG_PADDLE = 'big_paddle'
    EXTRA_LIFE = 'extra_life'


class BrickAttributes:
    SHAPE = Shape.SQUARE.value
    WIDTH = 20
    LENGTH = 3
    SPACING = 5
    NORMAL_SCORE = 10
    BROKEN_SCORE = 30
    STRONG_SCORE = 50


class PaddleAttributes:
    WIDTH = 20
    DEFAULT_LENGTH = 5
    MIN_ANGLE = 15
    MAX_ANGLE = 165
    COLOR = Color.YELLOW.value
    LASER_PADDLE_COLOR = Color.RED.value
    SHAPE = Shape.SQUARE.value
    START_POSITION = (0, SCREEN_BOTTOM_EDGE + WIDTH)


class BallAttributes:
    ANIMATION_SPEED = 50
    DEFAULT_SPEED = 1
    SIZE = 20
    RADIUS = SIZE / 2
    COLOR = Color.WHITE.value
    SHAPE = Shape.CIRCLE.value
    START_POSITION = (0, SCREEN_BOTTOM_EDGE + PaddleAttributes.WIDTH + SIZE)


class PowerupAttributes:
    SHAPE = Shape.ARROW.value
    COLOR = Color.YELLOW.value
    SPEED = 1.5
    WIDTH = 20
    IMAGE_TIME_LIMIT = 750
    IMAGE_SPEED = -1


class LaserAttributes:
    SHAPE = Shape.ARROW.value
    COLOR = Color.ORANGE.value
    SPEED = 1.5
    WIDTH = 20
    TIME_LIMIT = 20000
    FREQUENCY = 2000
