from turtle import Turtle, Screen
import time 
import random
from tkinter import messagebox
from pathlib import Path

messagebox.showinfo("Star Chaser", "⚠️ You are about to play high intensity space combat simulation ⚠️\n'a'/'d' - left/right\n's' - stop\n'space' - regular shot\n'e' - super shot\n'p' - pause for 10 seconds")

# Setting constants
WIDTH = 1000
HEIGHT = 1000
HEAD_SPEED = 0.7          # Number of pixels the head moves per frame
STAR_FALL_SPEED = 0.5
BULLET_SPEED = 7
SPECIAL_BULLET_SPEED = 10

# Opening file with saved highest score
file = Path("highest_score_save.txt")
saved_highest_core = int(file.read_text())

# Initializing game values dictionary
game_variables = {
    "points": 0,
    "shot_counter": 70,
    "super_counter": 10,
    "highest_points": saved_highest_core
}

# ================== DISPLAY SETTINGS ==================
# Screen settings
screen = Screen()
screen.bgcolor("black")
screen.tracer(False)
screen.title("Star Chaser")
screen.register_shape("star.gif")
screen.bgpic("background.gif")
screen.setup(WIDTH, HEIGHT)

# Score sign template
def score_sign_template(object, x, y):
    object.penup()
    object.hideturtle()
    object.color("white")
    object.goto(x, y)
    
score_sign = Turtle()
score_sign_template(score_sign, 0, 450)
score_sign.write(f"Points: {game_variables['points']}", align="center", font=("Calibri", 18))
score_sign2 = Turtle()                                                                                                     # Dont mind the assymetrical cors its little weird but it works good
score_sign_template(score_sign2, 355, 400)
score_sign2.write(f"Super shots left: {game_variables['super_counter']}", align="center", font=("Calibri", 18))
score_sign3 = Turtle()
score_sign_template(score_sign3, -405, 450)
score_sign3.write(f"Highest: {game_variables['highest_points']}", align="center", font=("Calibri", 18))
score_sign4 = Turtle()
score_sign_template(score_sign4, 385, 450)
score_sign4.write(f"Shots left: {game_variables['shot_counter']}", align="center", font=("Calibri", 18))

def update_score_sign(score_sign, score_sign3):
    score_sign.clear()
    score_sign.write(f"Points: {game_variables['points']}", align="center", font=("Calibri", 18))

    if score_sign3 != None:
        score_sign3.clear()
        score_sign3.write(f"Highest: {game_variables['highest_points']}", align="center", font=("Calibri", 18))

    screen.update()

# ================== GAME OBJECT SETTINGS ==================
# Object template
def object_template(object, color, x, y, size):
    object.penup()
    object.color(color)
    object.teleport(x, y)
    object.shapesize(size)

# Head settings
head = Turtle()
object_template(head, "red", 0, -300, 1)
head.shapesize(stretch_wid=4, stretch_len=5)
head.left(90)
head.direction = "stop"
head.speed(1)

# Star settings
star = Turtle("star.gif")
star.penup()
def spawn_star():
    star.teleport(random.randint(-480, 480), 620)

# Bullet settings
bullet = Turtle("square")
object_template(bullet, "lime", 0, 1000, 0.4)
special_bullet = Turtle("square")
object_template(special_bullet, "LightBlue", 0, 1000, 0.4)

# ================== MOVE FUNCTIONS ==================
def move():
    if head.direction == "left":
        x = head.xcor()
        head.setx(x - HEAD_SPEED)
    elif head.direction == "right":
        x = head.xcor()
        head.setx(x + HEAD_SPEED)

def stop():
    head.direction = "stop"
def move_left():
    head.direction = "left"
def move_right():
    head.direction = "right"         

# ================== SHOT FUNCTIONS ==================
def shot():
    if game_variables['shot_counter'] > 0:
        game_variables['shot_counter'] -= 1
        bullet.goto(head.xcor(), head.ycor())
        score_sign4.clear()
        score_sign4.write(f"Shots left: {game_variables['shot_counter']}", align="center", font=("Calibri", 18))

def shot2():
    if head.distance(star) > 250:
        if game_variables['super_counter'] > 0:
            game_variables['super_counter'] -= 1
            special_bullet.goto(head.xcor(), head.ycor())
            score_sign2.clear()
            score_sign2.write(f"Super shots left: {game_variables['super_counter']}", align="center", font=("Calibri", 18))


# Pause function
def pause():
    screen.update()
    for i in range(10, 0, -1):
        score_sign.clear()
        score_sign.write(f"{i}", align="center", font=("Calibri", 23))
        screen.update()
        time.sleep(1)
    update_score_sign(score_sign, None)

# ================== KEY BINDING ==================
screen.listen()
screen.onkeypress(stop, "s")
screen.onkeypress(move_left, "a")
screen.onkeypress(move_right, "d")
screen.onkeypress(shot, "space")
screen.onkeypress(shot2, "e")
screen.onkeypress(pause, "p")

# ================== COLLISION CHECKER ==================
def check_collision():

    # Border check
    if head.xcor() < -480 or head.xcor() > 478:
        if head.direction == "right":
            head.direction = "left"
        else: 
            head.direction = "right"

    # Star by body check
    if head.distance(star) < 30:
        game_variables['points'] += 1
        update_score_sign(score_sign, score_sign3)
        spawn_star()

    # Missed star check
    if star.ycor() < -505:
        game_variables['points'] = 0
        score_sign.clear()
        score_sign.write(f"Oh no", align="center", font=("Calibri", 18))
        screen.update()
        time.sleep(1)
        update_score_sign(score_sign, score_sign3)
        spawn_star()

    # Star by bullet check
    if bullet.distance(star) < 30: 
        game_variables['points'] += 1
        update_score_sign(score_sign, score_sign3)
        spawn_star()
        
    # Star by special bullet check
    if special_bullet.distance(star) < 25:
        game_variables['points'] += 3
        update_score_sign(score_sign, score_sign3)
        spawn_star()

    return game_variables['points']

# ================== MAIN GAME CYCLE ==================
while True:
    screen.update()

    if game_variables['points'] > game_variables['highest_points']:
        game_variables['highest_points'] = game_variables['points']
        file.write_text(str(game_variables['highest_points']))

    # Collisions handling
    game_variables['points'] = check_collision()

    # Objects moves
    bullet.sety(bullet.ycor() + BULLET_SPEED)
    special_bullet.sety(special_bullet.ycor() + SPECIAL_BULLET_SPEED)
    star.sety(star.ycor() - STAR_FALL_SPEED)

    move()
    time.sleep(0.00008)
