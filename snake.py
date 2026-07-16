from tkinter import *
import random 

GAME_WIDTH = 800
GAME_HEIGHT = 800
GAME_SPEED = 80
GAME_SIZE = 20
SNAKE_BODY = 3
SNAKE_COLOUR = "green"
FOOD_COLOUR = "red"
BACKGROUND_COLOUR = "black"


class Snake:
    
    def __init__(self):
        self.body_size = SNAKE_BODY
        self.coordinates = []
        self.squares = []

        for i in range (0, SNAKE_BODY):
            self.coordinates.append([0,0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, 
                x + GAME_SIZE, y + GAME_SIZE, 
                fill=SNAKE_COLOUR,
            )
            self.squares.append(square)

class Food:

    def __init__(self):

        x = random.randint(0, (GAME_WIDTH // GAME_SIZE) - 1) * GAME_SIZE
        y = random.randint(0, (GAME_HEIGHT // GAME_SIZE) - 1) * GAME_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(
            x, y,
            x + GAME_SIZE, y + GAME_SIZE,
            fill=FOOD_COLOUR,
            tag="food"
        )

def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= GAME_SIZE
    
    elif direction == "down":
        y += GAME_SIZE

    elif direction  == "left":
        x -= GAME_SIZE
    
    elif direction == "right":
        x += GAME_SIZE
    
    
    snake.coordinates.insert(0,(x, y ))

    square = canvas.create_rectangle(x, y, x + GAME_SIZE, y + GAME_SIZE, fill=SNAKE_COLOUR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:

        global score
        score += 1
        label.config(text="Score:{}".format(score))
        
        canvas.delete("food")
        food = Food()
    
    else: 
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
        return

    else:
        window.after(GAME_SPEED, next_turn, snake, food)

def change_direction(new_direction):
    
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction 
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction 
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction 

def check_collisions(snake):
    
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True
    
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
        
    return False

def restart_game():
    global score, direction, snake, food

    score = 0
    direction = "down"

    label.config(text=f"Score: {score}")

    canvas.delete(ALL)

    snake = Snake()
    food = Food()

    next_turn(snake, food)

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, 
                       font=('arial', 40), 
                       text="Game Over :( ",
                       fill="red",
                       tag="gameover",
                       )
    
    restart_button = Button(
        window,
        text="Restart",
        font=('arial', 20),
        command=restart_game,
        bg="blue",
        fg="white"
     )
    
    canvas.create_window(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2 + 50,
        window=restart_button,
        tag="restart"
    )
 
window = Tk()
window.title("Snake by Aron Armas")

score = 0 
direction =  "down"

label = Label(window, text="Score:{}".format(score), font=('arial', 40))
label.pack()
canvas = Canvas(window, bg=BACKGROUND_COLOUR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))


snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()