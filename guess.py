"""A simple number guessing game."""

import random

# The range the secret number can fall in (inclusive on both ends)
LOWEST = 1
HIGHEST = 100


def main():
    # Pick a random secret number within the range
    secret_number = random.randint(LOWEST, HIGHEST)

    # Keep track of how many guesses the player has made
    attempts = 0

    print(f"I'm thinking of a number between {LOWEST} and {HIGHEST}.")

    # Keep asking the player to guess until they get it right
    has_won = False
    while not has_won:
        # Ask the player for a guess as text, exiting cleanly on Ctrl+C / Ctrl+D
        try:
            guess_text = input("Your guess: ")
        except (EOFError, KeyboardInterrupt):
            print("\nThanks for playing!")
            break

        # Make sure the player actually typed a whole number
        try:
            guess = int(guess_text)
        except ValueError:
            print("Please enter a whole number.")
            continue

        # Reject out-of-range guesses without counting them as an attempt
        if guess < LOWEST or guess > HIGHEST:
            print(f"Please guess a number between {LOWEST} and {HIGHEST}.")
            continue

        attempts = attempts + 1

        # Compare the guess to the secret number and give a hint
        if guess < secret_number:
            print("Too low!")
        elif guess > secret_number:
            print("Too high!")
        else:
            has_won = True

    # Tell the player they won and how many guesses it took (only if they won)
    if has_won:
        attempt_word = "attempt" if attempts == 1 else "attempts"
        print(f"You got it! The number was {secret_number}.")
        print(f"It took you {attempts} {attempt_word}.")


if __name__ == "__main__":
    main()
