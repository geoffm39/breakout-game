from turtle import RawTurtle

from constants import (
   PowerupType
)


class Powerup(RawTurtle):
    def __init__(self, canvas, **kwargs):
        super().__init__(canvas, **kwargs)
