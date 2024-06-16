import tkinter as tk
import pygame
import random

# Constants for window and game elements
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SIZE = 30
# Increase paddle move distance
PADDLE_MOVE_DISTANCE = 50  
# Increase initial ball speed
INITIAL_BALL_SPEED_X = 4   
INITIAL_BALL_SPEED_Y = 4

# Initialize Pygame mixer
pygame.mixer.init()

# Load sound effects
score_sound = pygame.mixer.Sound("score.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")

def main():
    global game_over
    game_over = True

    window = create_window()
    canvas = create_canvas(window)
    paddles = draw_paddles(canvas)
    ball = draw_ball(canvas)
    scores = draw_scores(canvas)

    bind_keys(window, canvas, paddles)

    canvas.bind("<Button-1>", lambda event: start_stop_game(event, canvas, paddles, ball, scores))

    window.mainloop()

def create_window():
    #Create and return the main window.
    window = tk.Tk()
    window.title("Pong Game")
    window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    return window

def create_canvas(window):
    #Create and return the main canvas for drawing game elements. 
    canvas = tk.Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="blue")
    canvas.pack()
    return canvas

def draw_paddles(canvas):
    #Draw and return the paddles on the canvas. 
    paddle_left_x1 = 50
    paddle_left_y1 = (WINDOW_HEIGHT - PADDLE_HEIGHT) / 2
    paddle_left_x2 = paddle_left_x1 + PADDLE_WIDTH
    paddle_left_y2 = paddle_left_y1 + PADDLE_HEIGHT

    paddle_right_x1 = WINDOW_WIDTH - 50 - PADDLE_WIDTH
    paddle_right_y1 = (WINDOW_HEIGHT - PADDLE_HEIGHT) / 2
    paddle_right_x2 = paddle_right_x1 + PADDLE_WIDTH
    paddle_right_y2 = paddle_right_y1 + PADDLE_HEIGHT

    paddle_left = canvas.create_rectangle(paddle_left_x1, paddle_left_y1, paddle_left_x2, paddle_left_y2, fill="yellow")
    paddle_right = canvas.create_rectangle(paddle_right_x1, paddle_right_y1, paddle_right_x2, paddle_right_y2, fill="yellow")

    return paddle_left, paddle_right

def draw_ball(canvas):
    #Draw and return the ball on the canvas. 
    ball_x1 = (WINDOW_WIDTH - BALL_SIZE) / 2
    ball_y1 = (WINDOW_HEIGHT - BALL_SIZE) / 2
    ball_x2 = ball_x1 + BALL_SIZE
    ball_y2 = ball_y1 + BALL_SIZE

    ball = canvas.create_oval(ball_x1, ball_y1, ball_x2, ball_y2, fill="red")
    return ball

def draw_scores(canvas):
    #Draw and return the initial scores on the canvas. 
    score_left = canvas.create_text(WINDOW_WIDTH / 4, 50, text="0", fill="black", font=("Helvetica", 24))
    score_right = canvas.create_text(3 * WINDOW_WIDTH / 4, 50, text="0", fill="black", font=("Helvetica", 24))
    return score_left, score_right

def start_stop_game(event, canvas, paddles, ball, scores):
    #Start or stop the game based on a mouse click event.
    global game_over
    if game_over:
        game_over = False
        start_game(canvas, paddles, ball, scores)
    else:
        game_over = True
        canvas.delete("all")  # Clear canvas
        paddles = draw_paddles(canvas)
        ball = draw_ball(canvas)
        scores = draw_scores(canvas)

def bind_keys(window, canvas, paddles):
    #Bind keys for paddle movement to the window.
    paddle_left, paddle_right = paddles
    window.bind("<Up>", lambda event: move_paddle(canvas, paddle_right, -PADDLE_MOVE_DISTANCE))
    window.bind("<Down>", lambda event: move_paddle(canvas, paddle_right, PADDLE_MOVE_DISTANCE))
    window.bind("<KeyPress-w>", lambda event: move_paddle(canvas, paddle_left, -PADDLE_MOVE_DISTANCE))
    window.bind("<KeyPress-s>", lambda event: move_paddle(canvas, paddle_left, PADDLE_MOVE_DISTANCE))

def move_paddle(canvas, paddle, distance):
    # the specified paddle by the given distance on the canvas.
    canvas.move(paddle, 0, distance)
    paddle_coords = canvas.coords(paddle)
    if paddle_coords[1] < 0:
        canvas.move(paddle, 0, -paddle_coords[1])
    elif paddle_coords[3] > WINDOW_HEIGHT:
        canvas.move(paddle, 0, WINDOW_HEIGHT - paddle_coords[3])

def start_game(canvas, paddles, ball, scores):
    #Start the game by moving the ball and updating its position. 
    move_ball(canvas, paddles, ball, INITIAL_BALL_SPEED_X, INITIAL_BALL_SPEED_Y, scores, [0, 0])

def move_ball(canvas, paddles, ball, dx, dy, scores, score_values):
    #Move the ball on the canvas, handle collisions, and update scores. 
    global game_over
    if not game_over:
        canvas.move(ball, dx, dy)
        ball_coords = canvas.coords(ball)

        # Check for collisions with top and bottom walls
        if ball_coords[1] <= 0 or ball_coords[3] >= WINDOW_HEIGHT:
            dy = -dy

        # Check for collisions with paddles
        paddle_left, paddle_right = paddles
        paddle_left_coords = canvas.coords(paddle_left)
        paddle_right_coords = canvas.coords(paddle_right)

        if (ball_coords[0] <= paddle_left_coords[2] and ball_coords[1] >= paddle_left_coords[1] and ball_coords[3] <= paddle_left_coords[3]) or \
           (ball_coords[2] >= paddle_right_coords[0] and ball_coords[1] >= paddle_right_coords[1] and ball_coords[3] <= paddle_right_coords[3]):
            dx = -dx
            dy += random.choice([-0.5, 0.5])  # Adjust ball direction

        # Check for scoring
        if ball_coords[0] <= 0:
            score_values[1] += 1  # Right player scores
            update_scores(canvas, scores, score_values)
            reset_ball(canvas, ball)
            pygame.mixer.Sound.play(score_sound)
        elif ball_coords[2] >= WINDOW_WIDTH:
            score_values[0] += 1  # Left player scores
            update_scores(canvas, scores, score_values)
            reset_ball(canvas, ball)
            pygame.mixer.Sound.play(score_sound)

        # Check for game over condition
        if score_values[0] >= 5 or score_values[1] >= 5:
            game_over = True
            pygame.mixer.Sound.play(game_over_sound)
            canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, text="Game Over!", fill="black", font=("Helvetica", 36))
            return
        
        # Continue moving the ball after a short delay
        canvas.after(20, move_ball, canvas, paddles, ball, dx, dy, scores, score_values)

def update_scores(canvas, scores, score_values):
    #Update the scores displayed on the canvas.
    score_left, score_right = scores
    canvas.itemconfig(score_left, text=str(score_values[0]))
    canvas.itemconfig(score_right, text=str(score_values[1]))

def reset_ball(canvas, ball):
    #Reset the ball's position to the center of the canvas. 
    canvas.coords(ball, (WINDOW_WIDTH - BALL_SIZE) / 2, (WINDOW_HEIGHT - BALL_SIZE) / 2,
                  (WINDOW_WIDTH + BALL_SIZE) / 2, (WINDOW_HEIGHT + BALL_SIZE) / 2)

if __name__ == '__main__':
    main()
