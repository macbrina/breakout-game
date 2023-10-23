from turtle import Turtle, Screen

class Scoreboard():
    def __init__(self):
        super().__init__()
        self.score = 0
        self.countdown = 300
        self.minutes = self.countdown // 60
        self.seconds = self.countdown % 60
        self.level = 1
        self.lives = 3
        self.game_over = False
        self.highscore = 0
        self.save_score = False
        self.pause_time = False
        self.hits = 0
        self.screen = Screen()
        self.highscore_count = Turtle()
        self.score_count = Turtle()
        self.time_count = Turtle()
        self.score_display = Turtle()
        self.record_highscore()

    def show_score(self):
        self.score_count.clear()
        self.score_count.color("white")
        self.score_count.hideturtle()
        self.score_count.penup()
        self.score_count.goto(-300, 340)
        self.score_count.write(f"{self.score:03}", align="center", font=("Courier", 30, "bold"))

    def show_highscore(self):
        self.highscore_count.clear()
        self.highscore_count.color("white")
        self.highscore_count.hideturtle()
        self.highscore_count.penup()
        self.highscore_count.goto(280, 340)
        self.highscore_count.write(f"HS: {self.highscore:03}", align="center", font=("Courier", 30, "bold"))

    def timeframe(self):
        self.time_count.clear()
        self.time_count.color("white")
        self.time_count.hideturtle()
        self.time_count.penup()
        self.time_count.goto(0, 340)
        self.time_count.write(f"{self.minutes:02}:{self.seconds:02}", align="center", font=("Courier", 30, "bold"))

    def start_count_down(self):
        if self.countdown > 0 and not self.pause_time:
            self.minutes = self.countdown // 60
            self.seconds = self.countdown % 60
            self.countdown -= 1
            self.timeframe()
            self.screen.ontimer(self.start_count_down, 1000)

    def display_score(self):
        if self.lives > 0:
            live_bonus = 500 * int(self.lives)
        else:
            live_bonus = self.lives

        level_bonus = 500 * int(self.level)
        total_score = int(self.score) + live_bonus + level_bonus

        self.score_display.color("white")
        self.score_display.hideturtle()
        self.time_count.penup()
        self.time_count.goto(0, -170)
        self.time_count.write(f"SCORE BONUS: {self.score}", align="center", font=("Courier", 20, "bold"))
        self.time_count.goto(0, -200)
        self.time_count.write(f"LIVE BONUS: {live_bonus}", align="center", font=("Courier", 20, "bold"))
        self.time_count.goto(0, -230)
        self.time_count.write(f"LEVEL BONUS: {level_bonus}", align="center", font=("Courier", 20, "bold"))
        self.time_count.goto(0, -260)
        self.time_count.write(f"TOTAL SCORE: {total_score}", align="center", font=("Courier", 20, "bold"))


    def add_score(self, points):
        self.score += points
        self.show_score()

    def decrease_lives(self):
        if self.lives <= 0:
            self.lives = 0
        else:
            self.lives -= 1
        self.show_score()

    def level_up(self):
        self.level += 1

        if self.score > self.highscore:
            self.save_score = True
            self.highscore = self.score
            self.record_highscore()
        self.show_score()
        self.show_highscore()

    def reset_scoreboard(self):
        if int(self.score) > int(self.highscore):
            self.save_score = True
            self.highscore = self.score
            self.record_highscore()

        self.level = 1
        self.score = 0
        self.lives = 3
        self.countdown = 180
        self.hits = 0
        self.game_over = False
        self.pause_time = False
        self.show_score()
        self.show_highscore()

    def record_highscore(self):
        """Save highscore to data"""
        try:
            if self.save_score:
                with open("data.txt", "w") as file:
                    file.write(f"{self.highscore}")
                    self.save_score = False
            else:
                with open("data.txt", "r") as file:
                    score = file.read()
                    self.highscore = int(score)

        except FileNotFoundError:
            with open("data.txt", "w") as file:
                file.write("0")
