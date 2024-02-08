from constants import BRICK_COLOR, TYPE, NORMAL, STRONG, BARRIER, SPACING, SPACE_SIZE


class Levels:
    def __init__(self):
        self.current_level = 1

        self.level_1 = [
            [{TYPE: SPACING, SPACE_SIZE: 1080}],
            [{TYPE: NORMAL, BRICK_COLOR: 'blue'}]  # add color constants
        ]