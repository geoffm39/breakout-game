class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.configure(background='black')
        self.configure_screen()



        self.current_level = 1


        self.start_game()




    def start_game(self):
        self.add_level_bricks()
        self.balls.append(Ball(self.screen))
        self.update_game_screen()





    def update_game_screen(self):
        self.screen.update()
        for ball in self.balls:
            ball.move()
            self.check_for_paddle_contact(ball)
            self.check_for_wall_contact(ball)
            if self.ball_missed(ball):
                return
        self.after(3, self.update_game_screen)


