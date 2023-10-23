from turtle import Turtle
import random

RANDOM_POSITIONS = [(-240, 0), (270, 0), (-250, 0), (0, 0), (-50, 0), (-100, 0), (100, 0),
                    (200, 0), (150, 0), (50, 0)]

POSITION = random.choice(RANDOM_POSITIONS)


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("white")
        self.hideturtle()
        self.penup()
        self.setpos(POSITION)
        self.speed = 5  # Initial speed
        self.velocity = [5, 5]  # Initial velocity

    def move_ball(self):
        x, y = self.pos()
        self.goto(x + self.velocity[0], y + self.velocity[1])

    def bounce_y(self):
        self.velocity[1] *= -1

    def bounce_x(self):
        self.velocity[0] *= -1

    def increase_speed(self):
        self.velocity[0] *= 1.2  # Double the speed in the x-direction
        self.velocity[1] *= 1.2  # Double the speed in the y-direction

    def reset_position(self):
        self.goto(POSITION)
        self.velocity[0] = random.choice([5, -5])  # Randomize the x-direction
        self.velocity[1] = abs(self.velocity[1])  # Make sure the y-direction is upward

    def miss_turn(self):
        self.goto(POSITION)
        self.velocity[1] = abs(self.velocity[1])

    def level_up(self):
        """Increase the next level speed"""
        self.goto(POSITION)
        self.velocity[0] = random.choice([6, -6])
        self.velocity[1] = abs(self.velocity[1])
