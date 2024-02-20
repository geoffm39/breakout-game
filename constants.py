from enum import Enum


IMAGE_DIRECTORY = 'images/image-files'
BACKGROUND_FILENAME = 'background.jpg'

SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1080

SCREEN_LEFT_EDGE = -SCREEN_WIDTH / 2
SCREEN_RIGHT_EDGE = SCREEN_WIDTH / 2
SCREEN_TOP_EDGE = SCREEN_HEIGHT / 2 - 50
SCREEN_BOTTOM_EDGE = -SCREEN_HEIGHT / 2

PADDLE_WIDTH = 20
PADDLE_LENGTH = 5
MIN_PADDLE_ANGLE = 15
MAX_PADDLE_ANGLE = 165
PADDLE_COLOR = 'yellow'
PADDLE_SHAPE = 'square'
PADDLE_START_POSITION = (0, SCREEN_BOTTOM_EDGE + PADDLE_WIDTH)

BALL_SPEED = 1
BALL_SIZE = 20
BALL_RADIUS = BALL_SIZE / 2
BALL_COLOR = 'white'
BALL_SHAPE = 'circle'
BALL_START_POSITION = (0, SCREEN_BOTTOM_EDGE + PADDLE_WIDTH + BALL_SIZE)

SPACING = 'spacing'
SPACE_SIZE = 'space_size'

TYPE = 'type'
NORMAL = 'normal'
STRONG = 'strong'
BROKEN = 'broken'
BARRIER = 'barrier'

BRICK_COLOR = 'brick_color'
BLUE = 'blue'
RED = 'red'
YELLOW = 'yellow'
ORANGE = 'orange'
GREEN = 'green'
PURPLE = 'purple'

BRICK_SHAPE = 'square'
BRICK_WIDTH = 20
BRICK_LENGTH = 3

BRICK_SPACING = 5

VERTICAL_SURFACE = 'vertical'
HORIZONTAL_SURFACE = 'horizontal'
EAST = 0
NORTH = 90
WEST = 180
SOUTH = 270
COMPLETE_ANGLE = 360

POWERUP_SHAPE = 'arrow'
POWERUP_COLOR = 'white'
POWERUP_SPEED = 1.5


class PowerupType(Enum):
    MULTIBALL = 'multiball'
    FIREBALL = 'fireball'
    SLOW_BALL = 'slow_ball'
    FAST_BALL = 'fast_ball'
    LASERS = 'lasers'
    SMALL_PADDLE = 'small_paddle'
    BIG_PADDLE = 'big_paddle'
    EXTRA_LIFE = 'extra_life'
