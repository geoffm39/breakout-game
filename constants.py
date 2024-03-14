from enum import Enum


SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1080

SCREEN_LEFT_EDGE = -SCREEN_WIDTH / 2
SCREEN_RIGHT_EDGE = SCREEN_WIDTH / 2
SCREEN_TOP_EDGE = SCREEN_HEIGHT / 2 - 50
SCREEN_BOTTOM_EDGE = -SCREEN_HEIGHT / 2
SCREEN_CENTER = (0, 0)

EAST = 0
NORTH = 90
WEST = 180
SOUTH = 270
COMPLETE_ANGLE = 360

STARTING_LIVES = 3
MAX_LIVES = 5

SPACING = 'spacing'
SPACE_SIZE = 'space_size'
TYPE = 'type'
BRICK_COLOR = 'brick_color'
VERTICAL_SURFACE = 'vertical'
HORIZONTAL_SURFACE = 'horizontal'
TITLE = 'Breakout!'


class Color(Enum):
    BLUE = 'blue'
    RED = 'red'
    YELLOW = 'yellow'
    ORANGE = 'orange'
    GREEN = 'green'
    PURPLE = 'purple'
    WHITE = 'white'
    BLACK = 'black'


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


class FilePaths:
    IMAGE_DIRECTORY = 'images/image-files'
    BACKGROUND = 'background.jpg'
    POWERUP = 'powerup.png'
    PADDLE = 'paddle.png'
    PADDLE_LASERS = 'paddle-lasers.png'
    LASER = 'laser.png'
    FIREBALL = 'fireball.gif'
    BALL = 'ball.gif'
    LIVES = 'lives.png'
    HIGHSCORE = 'highscore.txt'
    GAME_OVER = 'game-over.png'
    BUTTON_OUTLINE = 'button-outline.png'
    START_GAME_BUTTON_OUTLINE = 'start-game-button.png'
    CONTROLS_BUTTON_OUTLINE = 'controls-button-outline.png'
    LOGO = 'logo.png'
    ICON = 'gui/arcade_icon.ico'


class TextAttributes:
    LIVES_POSITION = (SCREEN_RIGHT_EDGE - 50, SCREEN_HEIGHT / 2 - 46)
    LIVES_IMAGE_X_COORD = SCREEN_RIGHT_EDGE - 105
    LIVES_IMAGE_Y_COORD = (SCREEN_TOP_EDGE + 26) * -1
    SCORE_POSITION = (0, SCREEN_HEIGHT / 2 - 46)
    HIGHSCORE_POSITION = (SCREEN_LEFT_EDGE + 50, SCREEN_HEIGHT / 2 - 46)
    HIGHSCORE_NOTIFICATION_TEXT_POSITION = (0, -100)
    HIGHSCORE_NOTIFICATION_TEXT = 'High Score!'
    SCORE_NOTIFICATION_TEXT = 'Score:'
    QUIT_GAME_TEXT_POSITION = (-200, -200)
    QUIT_GAME_TEXT = 'Quit?'
    QUIT_GAME_FONT = ('Verdana', 21, 'bold')
    YES_BUTTON_POSITION = (0, -200)
    YES_BUTTON_OUTLINE_POSITION = (0, 200)
    YES_BUTTON_TEXT = 'Yes'
    NO_BUTTON_TEXT = 'No'
    NO_BUTTON_POSITION = (200, -200)
    NO_BUTTON_OUTLINE_POSITION = (180, 200)
    BUTTON_FONT = ('Verdana', 18, 'bold')
    GAME_FONT = ('Verdana', 30, 'bold')
    START_GAME_BUTTON_FONT = ('Verdana', 24, 'bold')
    START_GAME_BUTTON_TEXT = 'Start Game'
    START_GAME_BUTTON_POSITION = (0, -8)
    CONTROLS_TEXT = 'Controls:'
    CONTROLS_TEXT_FONT = ('Verdana', 21, 'bold')
    KEYBOARD_BUTTON_TEXT = 'Keyboard'
    MOUSE_BUTTON_TEXT = 'Mouse'
    CONTROLS_TEXT_POSITION = (-300, -130)
    KEYBOARD_BUTTON_POSITION = (0, -130)
    KEYBOARD_BUTTON_OUTLINE_POSITION = (0, 140)
    MOUSE_BUTTON_POSITION = (280, -130)
    MOUSE_BUTTON_OUTLINE_POSITION = (236, 140)
    LOGO_POSITION = (0, -130)


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
    SPEED = 10
    MOVEMENT = 10


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
