from turtle import RawTurtle

from constants import (
   MULTIBALL, FIREBALL, SLOW_BALL, FAST_BALL, LASERS, SMALL_PADDLE, BIG_PADDLE, EXTRA_LIFE
)


class Powerup(RawTurtle):
    def __init__(self, canvas, **kwargs):
        super().__init__(canvas, **kwargs)
