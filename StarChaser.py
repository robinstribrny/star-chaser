from turtle import Turtle, Screen
import time 
import random
from tkinter import messagebox

messagebox.showinfo("Star Chaser", "⚠️ You are about to play high intensity space combat simulation ⚠️\n'a'/'d' - left/right\n's' - stop\n'space' - regular shot\n'e' - super shot\n'p' - pause for 10 seconds")

# Variable initialization
points = 0
plus_points = 0
global super_counter
super_counter = 10
highest_points = 0 

# Screen settings
screen = Screen()
screen.bgcolor("black")
screen.tracer(False)
screen.title("Star Chaser")
screen.register_shape("star.gif")
screen.bgpic("background.gif")
screen.setup(1200, 1200)

# Head settings
head = Turtle()
head.shapesize(1)
head.left(90)
head.color("red")
head.shapesize(stretch_wid=4, stretch_len=5)
head.direction = ""
head.speed(1)
head.penup()
head.teleport(y=-400)

# Star settings
star = Turtle("star.gif")
star.penup()

# Bullet settings
bullet = Turtle("square")
bullet.shapesize(0.4)
bullet.color("lime")
bullet.penup()
bullet.teleport(0, 1000)
special_bullet = Turtle("square")
special_bullet.shapesize(0.4)
special_bullet.color("orange")
special_bullet.penup()
special_bullet.teleport(0, 1000)

# Display settings
score_sign = Turtle()
score_sign.color("white")
score_sign.hideturtle()
score_sign.teleport(0, 500)
score_sign.write(f"Points: {points}", align="center", font=("Calibri", 18))
score_sign2 = Turtle()
score_sign2.color("white")
score_sign2.hideturtle()
score_sign2.teleport(400, 500)
score_sign2.write(f"Super shots left: {super_counter}", align="center", font=("Calibri", 18))
score_sign3 = Turtle()
score_sign3.color("white")
score_sign3.hideturtle()
score_sign3.teleport(-400, 500)
score_sign3.write(f"Highest: {highest_points}", align="center", font=("Calibri", 18))

# ====== Move Functions ======
def move():
    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 0.7)
    elif head.direction == "right":
        x = head.xcor()
        head.setx(x + 0.7)

def stop():
    head.direction = "stop"
def move_left():
    head.direction = "left"
def move_right():
    head.direction = "right"         

# ====== Shot Functions ======
def shot():
    bullet.goto(head.xcor(), head.ycor())
def shot2():
    global super_counter
    if head.distance(star) > 450:
        if super_counter > 0:
            super_counter -= 1
            special_bullet.goto(head.xcor(), head.ycor())
            score_sign2.clear()
            score_sign2.write(f"Super shots left: {super_counter}", align="center", font=("Calibri", 18)) 

# System function
def pause():
    screen.update()
    for i in range(10, 0, -1):
        screen.update()
        score_sign.clear()
        score_sign.write(f"{i}", align="center", font=("Calibri", 23))
        time.sleep(1)

# ====== Key Binding ======
screen.listen()
screen.onkeypress(stop, "s")
screen.onkeypress(move_left, "a")
screen.onkeypress(move_right, "d")
screen.onkeypress(shot, "space")
screen.onkeypress(shot2, "e")
screen.onkeypress(pause, "p")

# ====== Main Game Cycle ======
while True:
    screen.update()

    if points > highest_points:
        highest_points = points

    # Collisions handling
    if head.xcor() < -580 or head.xcor() > 580:
        if head.direction == "right":
            head.direction = "left"
        else: 
            head.direction = "right"

    if head.distance(star) < 30:
        points += 1
        star.teleport(random.randint(-580, 580), 620)
        score_sign.clear()
        score_sign.write(f"Points: {points}", align="center", font=("Calibri", 18))

    if bullet.distance(star) < 30: 
        if head.distance(bullet) < 200:
            plus_points = 1
        else:
            plus_points = 2
        points += plus_points
        star.teleport(random.randint(-580, 580), 620)
        score_sign.clear()
        score_sign.write(f"Points: {points}", align="center", font=("Calibri", 18))

    if special_bullet.distance(star) < 25:
        points += 3
        star.teleport(random.randint(-580, 580), 620)
        score_sign.clear()
        score_sign.write(f"Points: {points}", align="center", font=("Calibri", 18))

    # Missed star scenario handling
    if star.ycor() < -610:
        screen.update()
        score_sign.clear()
        points = 0
        score_sign.write(f"Oh no", align="center", font=("Calibri", 18))
        screen.update()
        time.sleep(1)
        score_sign.clear()
        score_sign.write(f"Points: {points}", align="center", font=("Calibri", 18))
        star.teleport(random.randint(-580, 580), 620)
        score_sign3.clear()
        score_sign3.write(f"Highest: {highest_points}", align="center", font=("Calibri", 18))

    # Objects moves
    bullet.sety(bullet.ycor() + 7)
    special_bullet.sety(special_bullet.ycor() + 10)
    star.sety(star.ycor() - 0.5)

    move()
    time.sleep(0.00008)

screen.exitonclick()