from turtle import Turtle

LEFT = "Left"
RIGHT = "Right"
MOVE_DISTANCE = 80
PADDLE_RIGHT_BORDER = 360
PADDLE_LEFT_BORDER = -360


class Paddle(Turtle):
    def __init__(self, position):
        super().__init__()
        self.color("blue")
        self.shape("square")
        self.shapesize(stretch_wid=1, stretch_len=7)
        self.penup()
        self.goto(position)
        self.start_pos = position

    def move_left(self):
        new_x = self.xcor() - MOVE_DISTANCE
        if new_x > PADDLE_LEFT_BORDER:
            self.setx(new_x)

    def move_right(self):
        new_x = self.xcor() + MOVE_DISTANCE
        if new_x < PADDLE_RIGHT_BORDER:
            self.setx(new_x)

    def reset_position(self):
        self.goto(self.start_pos)
