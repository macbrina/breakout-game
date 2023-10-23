from turtle import Turtle


class Bricks(Turtle):
    def __init__(self, xpos, ypos, color):
        super().__init__()
        self.shape("square")
        self.color(color)
        self.shapesize(stretch_wid=1, stretch_len=4)
        self.penup()
        self.goto(xpos, ypos)

    def delete(self):
        self.goto(4000, 4000)
