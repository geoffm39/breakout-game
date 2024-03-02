from turtle import RawTurtle

from constants import HIGHSCORE_FILENAME


class Scores(RawTurtle):
    def __init__(self, canvas, **kwargs):
        super().__init__(canvas, **kwargs)

        self.score = None
        self.highscore = self.load_highscore_from_file()

    @staticmethod
    def load_highscore_from_file():
        try:
            with open(HIGHSCORE_FILENAME, 'r') as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    def save_highscore_to_file(self):
        with open(HIGHSCORE_FILENAME, 'w') as file:
            file.write(str(self.highscore))
