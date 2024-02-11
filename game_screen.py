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



    @staticmethod
    def is_spacing(position):
        return position[TYPE] == SPACING

    def update_game_screen(self):
        self.screen.update()
        for ball in self.balls:
            ball.move()
            self.check_for_paddle_contact(ball)
            self.check_for_wall_contact(ball)
            if self.ball_missed(ball):
                return
        self.after(3, self.update_game_screen)

    def check_for_wall_contact(self, ball):
        if self.ball_hit_side_wall(ball):
            ball.bounce(VERTICAL_SURFACE)
        if self.ball_hit_top_wall(ball):
            ball.bounce(HORIZONTAL_SURFACE)

    def check_for_paddle_contact(self, ball):
        paddle_bbox = self.paddle.get_paddle_bbox()
        if self.ball_hit_paddle(ball, paddle_bbox):
            paddle_angle_modifier = self.paddle.get_paddle_modifier_angle(ball.xcor())
            ball.bounce(HORIZONTAL_SURFACE, paddle_angle_modifier)

    @staticmethod
    def ball_hit_paddle(ball, paddle_bbox):
        ball_x, ball_y = ball.pos()
        ball_bottom_y = int(ball_y - BALL_RADIUS)
        paddle_x1, paddle_y1, paddle_x2 = paddle_bbox[:3]
        return ball_bottom_y == paddle_y1 and paddle_x1 <= ball_x <= paddle_x2

    @staticmethod
    def ball_missed(ball):
        return ball.ycor() <= SCREEN_BOTTOM_EDGE + BALL_RADIUS

    @staticmethod
    def ball_hit_top_wall(ball):
        return ball.ycor() >= SCREEN_TOP_EDGE - BALL_RADIUS

    @staticmethod
    def ball_hit_side_wall(ball):
        return ball.xcor() >= SCREEN_RIGHT_EDGE - BALL_RADIUS or ball.xcor() <= SCREEN_LEFT_EDGE + BALL_RADIUS
