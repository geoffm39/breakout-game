from level_data import LEVELS


class Levels:
    def __init__(self):
        self.levels = LEVELS

    def get_level(self, level_number):
        return self.levels[level_number]
