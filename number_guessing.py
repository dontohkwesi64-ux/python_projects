import random  # allows us to generate random numbers

def number_guessing_game():
    print("Welcome to the Number Guessing Game!")
    print("I have selected a number between 1 and 100. Can you guess it?")

    secret_number = random.randint(1, 100)  # random number between 1 and 100
    attempts = 0

    while True:
        guess = input("Enter your guess (or type 'q' to quit): ")

        if guess.lower() == 'q':
            print(f"Goodbye! The number was {secret_number}.")
            break

        if not guess.isdigit():
            print("Please enter a valid number.")
            continue

        guess = int(guess)
        attempts += 1

        if guess < secret_number:
            print("Too low! Try again.")
        elif guess > secret_number:
            print("Too high! Try again.")
        else:
            print(f"Congratulations! You guessed it in {attempts} attempts.")
            break

# Run the game
number_guessing_game()
