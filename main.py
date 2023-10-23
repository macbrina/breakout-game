from turtle import Screen, Terminator, Turtle
from paddle import Paddle
from bricks import Bricks
from ball import Ball
from scoreboard import Scoreboard

# from ui import run_game


UPPER_BORDER = 350
LEFT_BORDER = -350
RIGHT_BORDER = 350
BOTTOM_BORDER = -350
PADDLE_BORDER = -320
ROWS = 8
COLUMNS = 9
COLORS = ["red", "red", "orange", "orange", "green", "green", "yellow", "yellow"]
BRICK_DISTANCE = 23

POINTS = {
    "yellow": 25,
    "green": 50,
    "orange": 100,
    "red": 150
}


def check_collision(item_a, item_b):
    """Check the collision between ball and paddle"""
    w, h = 0, 0
    if item_b.turtlesize()[1] == 7:
        w = 60
        h = 20
    elif item_b.turtlesize()[1] == 4:
        w = 40
        h = 20
    elif item_b.turtlesize()[0] == 1:
        h = 13
    elif item_b.turtlesize()[0] < 1:
        h = 7
    return abs(item_a.xcor() - item_b.xcor()) < w and (item_a.ycor() - item_b.ycor()) < h


class Breakout:
    def __init__(self):
        self.screen = Screen()
        self.screen.title("Breakout")
        self.screen.bgcolor("Black")
        self.screen.setup(width=800, height=800)
        self.screen.tracer(0)

        self.ball = Ball()
        self.scoreboard = Scoreboard()

        self.paddle = Paddle((0, -350))
        # Listen for key press of the paddle
        self.screen.listen()
        self.screen.onkeypress(self.paddle.move_left, "Left")
        self.screen.onkeypress(self.paddle.move_right, "Right")
        self.screen.onkeypress(self.start_game, "s")
        self.screen.onkeypress(self.restart_game, "y")
        self.screen.onkeypress(self.toggle_game, "space")

        self.count = Turtle()
        self.ready_text = Turtle()
        self.pause = Turtle()
        self.is_over = Turtle()

        self.bricks = []
        self.x1 = -340
        self.y1 = 320 - BRICK_DISTANCE
        self.game_is_on = False
        self.is_paused = False
        self.game_restart = True
        self.hit_yellow = False
        self.hit_red = False
        self.get_ready_time = 3
        self.splash_screen = Turtle()
        self.splashscreen()

    def draw_bricks(self):
        for row in range(ROWS):
            y_val = self.y1 - row * 25
            color = COLORS[row // 1]
            for column in range(COLUMNS):
                x_val = self.x1 + column * (BRICK_DISTANCE + 61)
                bricks = Bricks(x_val, y_val, color)
                self.bricks.append(bricks)

    def run_timer(self):
        if self.get_ready_time >= 0:
            self.get_ready_time -= 1

    def toggle_game(self):
        """Toggle between play and pause"""
        self.is_paused = not self.is_paused
        self.scoreboard.pause_time = not self.scoreboard.pause_time
        if not self.is_paused:
            self.game_is_on = True
            self.scoreboard.start_count_down()
            self.play_game()

    def get_ready(self):
        """A countdown to show gets ready"""
        self.run_timer()
        self.count.clear()
        if self.get_ready_time >= 0:
            self.text_ready()
            self.count.color("white")
            self.count.hideturtle()
            self.count.pen()
            self.count.goto(0, -100)
            self.count.write(f"{self.get_ready_time}", align="center", font=("Courier", 25, "bold"))
            self.screen.ontimer(self.get_ready, 1000)
        else:
            self.ready_text.clear()
            self.game_is_on = True
            self.game_restart = False
            self.scoreboard.pause_time = False
            self.scoreboard.start_count_down()
            self.play_game()

    def text_ready(self):
        """Text to show get ready"""
        self.ready_text.color("white")
        self.ready_text.hideturtle()
        self.ready_text.penup()
        self.ready_text.goto(0, -50)
        self.ready_text.write("GET READY", align="center", font=("Courier", 25, "bold"))

    def splashscreen(self):
        """Splashscreen for initial game run"""
        self.splash_screen.hideturtle()
        self.splash_screen.color("white")
        self.splash_screen.penup()
        self.splash_screen.goto(0, 50)
        self.splash_screen.write("BREAKOUT", align="center", font=("Courier", 20, "bold"))
        self.splash_screen.goto(0, 0)
        self.splash_screen.write("Press S to Start", align="center", font=("Courier", 20, "bold"))
        self.screen.exitonclick()

    def pause_game(self):
        """Pause the game"""
        self.pause.hideturtle()
        self.pause.color("white")
        self.pause.penup()
        self.pause.goto(0, -100)
        self.pause.write("PAUSE", align="center", font=("Courier", 20, "bold"))

    def game_over(self):
        """Output Game over screen"""
        self.is_over.hideturtle()
        self.ball.hideturtle()
        self.screen.update()
        self.is_over.color("white")
        self.is_over.penup()
        self.is_over.goto(0, -50)
        self.is_over.write("TIME IS OVER", align="center", font=("Courier", 20, "bold"))
        # self.is_over.goto(0, -100)
        # self.is_over.write("GAME OVER", align="center", font=("Courier", 20, "bold"))
        self.is_over.goto(0, -100)
        self.is_over.write("Press Y to go again or Click random key to quit", align="center",
                           font=("Courier", 20, "bold"))
        self.scoreboard.display_score()
        self.screen.exitonclick()

    def start_game(self):
        """Start the game when after the pressing s on splashscreen"""
        if not self.game_is_on:
            self.splash_screen.clear()
            self.draw_bricks()
            self.scoreboard.show_score()
            self.scoreboard.show_highscore()
            self.scoreboard.timeframe()
            self.screen.update()
            self.get_ready()

    def restart_game(self):
        if self.game_restart:
            self.ball.reset_position()
            self.paddle.reset_position()
            self.hit_red = False
            self.hit_yellow = False
            self.is_over.clear()
            self.scoreboard.score_display.clear()
            self.get_ready_time = 3
            self.ball.hideturtle()
            self.scoreboard.reset_scoreboard()
            self.start_game()

    def play_game(self):
        while self.game_is_on:
            if self.is_paused:
                self.screen.update()
                self.pause_game()
            elif self.scoreboard.countdown <= 0:
                self.game_is_on = False
                self.ball.hideturtle()
                self.game_restart = True
                self.scoreboard.pause_time = True
                self.game_over()
            else:
                self.pause.clear()
                self.ball.showturtle()
                self.screen.update()
                self.ball.move_ball()

                # detect collision with left and right walls
                if self.ball.xcor() > RIGHT_BORDER or self.ball.xcor() < LEFT_BORDER:
                    self.ball.bounce_x()

                # detect collision with up
                if self.ball.ycor() > UPPER_BORDER:
                    self.ball.bounce_y()

                if check_collision(self.ball, self.paddle):
                    self.ball.bounce_y()

                # Check collision with bricks
                for brick in self.bricks:
                    if self.ball.distance(brick) < 40:
                        brick.delete()
                        self.bricks.remove(brick)
                        self.scoreboard.hits += 1
                        self.scoreboard.add_score(POINTS[brick.color()[0]])
                        self.ball.bounce_y()

                        if len(self.bricks) == 0:
                            self.scoreboard.level_up()
                            self.ball.level_up()

                            if not self.scoreboard.game_over:
                                self.game_is_on = False
                                self.start_game()
                            else:
                                self.game_is_on = False
                                self.game_restart = True
                                self.game_over()

                        # Check for hits and increase the speed of the ball
                        if self.scoreboard.hits == 4 or self.scoreboard.hits == 12:
                            self.ball.increase_speed()
                        if "yellow" in brick.color() and not self.hit_yellow:
                            self.ball.increase_speed()
                            self.hit_yellow = True
                        if "red" in brick.color() and not self.hit_red:
                            self.ball.increase_speed()
                            self.hit_red = True

                # Check when the ball has missed the paddle
                if self.ball.ycor() < -400:
                    self.scoreboard.decrease_lives()
                    self.ball.miss_turn()

                    # if self.scoreboard.game_over:
                    #     self.game_is_on = False
                    #     self.game_restart = True
                    #     self.scoreboard.pause_time = True
                    #     self.game_over()


if __name__ == "__main__":
    try:
        breakout = Breakout()
    except Terminator:
        pass
