from turtle import RawTurtle

from constants import (
    Color, TextAttributes, FilePaths, STARTING_LIVES, MAX_LIVES
)


class Scores(RawTurtle):
    def __init__(self, canvas, **kwargs):
        super().__init__(canvas, **kwargs)

        self.lives = STARTING_LIVES
        self.score = 0
        self.highscore = self.load_highscore_from_file()

        self.set_properties()

    def set_properties(self):
        self.color(Color.YELLOW.value)
        self.penup()
        self.hideturtle()

    @staticmethod
    def load_highscore_from_file():
        try:
            with open(FilePaths.HIGHSCORE, 'r') as file:
                return int(file.read())
        except FileNotFoundError:
            return 0

    def save_highscore_to_file(self):
        with open(FilePaths.HIGHSCORE, 'w') as file:
            file.write(str(self.highscore))

    def update_scores(self):
        self.clear()
        font = TextAttributes.GAME_FONT
        self.setposition(TextAttributes.HIGHSCORE_POSITION)
        self.write(self.highscore, align='left', font=font)
        self.setposition(TextAttributes.SCORE_POSITION)
        self.write(self.score, align='center', font=font)
        self.setposition(TextAttributes.LIVES_POSITION)
        self.write(self.lives, align='right', font=font)

    def increase_score(self, score):
        self.score += score
        self.update_scores()

    def check_for_highscore(self):
        if self.is_highscore():
            self.highscore = self.score
            self.save_highscore_to_file()
            self.show_game_over_highscore()

    def no_more_lives(self):
        return self.lives == 0

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

    def show_game_over_highscore(self):
        self.setposition(TextAttributes.HIGHSCORE_NOTIFICATION_TEXT_POSITION)
        self.write(TextAttributes.HIGHSCORE_NOTIFICATION_TEXT,
                   align='center',
                   font=TextAttributes.GAME_FONT)
        self.setposition(TextAttributes.HIGHSCORE_NOTIFICATION_VALUE_POSITION)
        self.write(self.highscore, align='center', font=TextAttributes.GAME_FONT)

    def is_highscore(self):
        return self.score > self.highscore
