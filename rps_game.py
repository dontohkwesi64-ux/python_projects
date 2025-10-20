import tkinter as tk
from PIL import Image, ImageTk
import random

# Initialize main window
window = tk.Tk()
window.title("Rock-Paper-Scissors Game")
window.geometry("500x400")

# Initialize scores
player_score = 0
computer_score = 0

# Function to determine winner
def determine_winner(player_choice, computer_choice):
    if player_choice == computer_choice:
        return "tie"
    elif (
        (player_choice == "rock" and computer_choice == "scissors") or
        (player_choice == "paper" and computer_choice == "rock") or
        (player_choice == "scissors" and computer_choice == "paper")
    ):
        return "player"
    else:
        return "computer"

# Function to handle player's move
def play(player_choice):
    global player_score, computer_score

    computer_choice = random.choice(["rock", "paper", "scissors"])
    winner = determine_winner(player_choice, computer_choice)

    if winner == "player":
        player_score += 1
        result_text.set(f"You win! Computer chose {computer_choice}.")
    elif winner == "computer":
        computer_score += 1
        result_text.set(f"Computer wins! Computer chose {computer_choice}.")
    else:
        result_text.set(f"It's a tie! Computer chose {computer_choice}.")

    score_text.set(f"Scores => You: {player_score} | Computer: {computer_score}")

# Function to reset the game
def reset_game():
    global player_score, computer_score
    player_score = 0
    computer_score = 0
    score_text.set(f"Scores => You: {player_score} | Computer: {computer_score}")
    result_text.set("Make your move!")

# Labels to display score and result
score_text = tk.StringVar()
score_text.set("Scores => You: 0 | Computer: 0")
score_label = tk.Label(window, textvariable=score_text, font=("Helvetica", 14))
score_label.pack(pady=10)

result_text = tk.StringVar()
result_text.set("Make your move!")
result_label = tk.Label(window, textvariable=result_text, font=("Helvetica", 14))
result_label.pack(pady=10)

# Load images
rock_img = ImageTk.PhotoImage(Image.open("rock.png").resize((80, 80)))
paper_img = ImageTk.PhotoImage(Image.open("paper.png").resize((80, 80)))
scissors_img = ImageTk.PhotoImage(Image.open("scissors.png").resize((80, 80)))

# Buttons with images
button_frame = tk.Frame(window)
button_frame.pack(pady=20)

tk.Button(button_frame, image=rock_img, command=lambda: play("rock")).grid(row=0, column=0, padx=10)
tk.Button(button_frame, image=paper_img, command=lambda: play("paper")).grid(row=0, column=1, padx=10)
tk.Button(button_frame, image=scissors_img, command=lambda: play("scissors")).grid(row=0, column=2, padx=10)

# Reset button
tk.Button(window, text="Reset Game", width=15, command=reset_game).pack(pady=10)

# Start the GUI loop
window.mainloop()
