from turtle import RawTurtle

from constants import (
    HIGHSCORE_FILENAME, YELLOW, SCORE_POSITION, LIVES_POSITION, HIGHSCORE_POSITION, STARTING_LIVES, MAX_LIVES, GAME_FONT
)


class Scores(RawTurtle):
    def __init__(self, canvas, **kwargs):
        super().__init__(canvas, **kwargs)

        self.lives = STARTING_LIVES
        self.score = 0
        self.highscore = self.load_highscore_from_file()

        self.set_properties()
        self.update_scores()

    def set_properties(self):
        self.color(YELLOW)
        self.penup()
        self.hideturtle()

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

    def update_scores(self):
        self.clear()
        self.setposition(HIGHSCORE_POSITION)
        self.write(self.highscore, align='left', font=GAME_FONT)
        self.setposition(SCORE_POSITION)
        self.write(self.score, align='center', font=GAME_FONT)
        self.setposition(LIVES_POSITION)
        self.write(self.lives, align='right', font=GAME_FONT)

    def increase_score(self, score):
        self.score += score
        self.update_scores()

    def check_for_highscore(self):
        if self.score > self.highscore:
            self.highscore = self.score
            self.save_highscore_to_file()

    def get_lives(self):
        return self.lives

    def decrease_lives(self):
        self.lives -= 1
        self.update_scores()

    def increase_lives(self):
        self.lives += 1
        if self.lives > MAX_LIVES:
            self.lives = MAX_LIVES
        self.update_scores()

    def reset_scores(self):
        self.lives = STARTING_LIVES
        self.score = 0
        self.highscore = self.load_highscore_from_file()
        self.update_scores()
