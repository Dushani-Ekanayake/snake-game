import turtle
import time
import random

# --- Game Configuration ---
SCREEN_SIZE = 600
SEGMENT_SIZE = 20
INITIAL_DELAY = 0.1
FONT = ("Courier", 24, "normal")


# ---------------- Snake Class ----------------
class Snake:
    def __init__(self):
        self.segments = []
        self.head = self._create_segment("black", (0, 0))
        self.direction = "stop"

    def _create_segment(self, color, position):
        segment = turtle.Turtle("square")
        segment.speed(0)
        segment.color(color)
        segment.penup()
        segment.goto(position)
        return segment

    def move(self):
        # Move the body segments backwards
        for idx in range(len(self.segments) - 1, 0, -1):
            x = self.segments[idx - 1].xcor()
            y = self.segments[idx - 1].ycor()
            self.segments[idx].goto(x, y)

        # Move first segment to head position
        if self.segments:
            self.segments[0].goto(self.head.xcor(), self.head.ycor())

        # Move the head
        x, y = self.head.xcor(), self.head.ycor()
        if self.direction == "up":
            self.head.sety(y + SEGMENT_SIZE)
        elif self.direction == "down":
            self.head.sety(y - SEGMENT_SIZE)
        elif self.direction == "left":
            self.head.setx(x - SEGMENT_SIZE)
        elif self.direction == "right":
            self.head.setx(x + SEGMENT_SIZE)

    def extend(self):
        new_segment = self._create_segment("grey", self.head.position())
        self.segments.append(new_segment)

    def reset(self):
        for seg in self.segments:
            seg.goto(1000, 1000)  # move offscreen
        self.segments.clear()
        self.head.goto(0, 0)
        self.direction = "stop"


# ---------------- Food Class ----------------
class Food(turtle.Turtle):
    def __init__(self):
        super().__init__("circle")
        self.speed(0)
        self.color("red")
        self.penup()
        self.refresh()

    def refresh(self):
        x = random.randint(-280, 280)
        y = random.randint(-280, 280)
        self.goto(x, y)


# ---------------- Scoreboard Class ----------------
class Scoreboard(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.high_score = 0
        self.hideturtle()
        self.color("white")
        self.penup()
        self.goto(0, 260)
        self.update()

    def update(self):
        self.clear()
        self.write(f"Score: {self.score}  High Score: {self.high_score}",
                   align="center", font=FONT)

    def increase(self, points=10):
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score
        self.update()

    def reset(self):
        self.score = 0
        self.update()


# ---------------- Game Class ----------------
class Game:
    def __init__(self):
        # Screen setup
        self.wn = turtle.Screen()
        self.wn.title("Snake Game")
        self.wn.bgcolor("green")
        self.wn.setup(width=SCREEN_SIZE, height=SCREEN_SIZE)
        self.wn.tracer(0)

        # Game objects
        self.snake = Snake()
        self.food = Food()
        self.scoreboard = Scoreboard()

        # Timing
        self.delay = INITIAL_DELAY

        # Controls
        self.bind_keys()

    def bind_keys(self):
        self.wn.listen()
        self.wn.onkeypress(lambda: self.change_direction("up"), "w")
        self.wn.onkeypress(lambda: self.change_direction("down"), "s")
        self.wn.onkeypress(lambda: self.change_direction("left"), "a")
        self.wn.onkeypress(lambda: self.change_direction("right"), "d")
        self.wn.onkeypress(lambda: self.change_direction("up"), "Up")
        self.wn.onkeypress(lambda: self.change_direction("down"), "Down")
        self.wn.onkeypress(lambda: self.change_direction("left"), "Left")
        self.wn.onkeypress(lambda: self.change_direction("right"), "Right")

    def change_direction(self, direction):
        opposite = {"up": "down", "down": "up", "left": "right", "right": "left"}
        if self.snake.direction != opposite.get(direction):
            self.snake.direction = direction

    def play(self):
        while True:
            self.wn.update()
            self.snake.move()

            # Border collision
            if abs(self.snake.head.xcor()) > 290 or abs(self.snake.head.ycor()) > 290:
                self.reset_game()

            # Food collision
            if self.snake.head.distance(self.food) < SEGMENT_SIZE:
                self.food.refresh()
                self.snake.extend()
                self.scoreboard.increase()
                if self.delay > 0.02:
                    self.delay -= 0.001

            # Body collision
            for seg in self.snake.segments:
                if seg.distance(self.snake.head) < SEGMENT_SIZE / 2:
                    self.reset_game()

            time.sleep(self.delay)

    def reset_game(self):
        time.sleep(1)
        self.snake.reset()
        self.scoreboard.reset()
        self.delay = INITIAL_DELAY


# ---------------- Run the Game ----------------
if __name__ == "__main__":
    Game().play()
