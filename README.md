# Guessing Game

A simple command-line number guessing game written for beginners, using
only Python's standard library.

## How it works

The computer picks a random number between 1 and 100. You type guesses
until you find it, and the game tells you "Too high!" or "Too low!"
after each one. When you guess correctly, it prints how many attempts
it took.

## Requirements

- Python 3

## Run it

```bash
python3 guess.py
```

## Notes

- Non-numeric input (e.g. `abc`) is rejected and doesn't count as an attempt.
- Out-of-range guesses (below 1 or above 100) are rejected and don't count
  as an attempt.
- Press Ctrl+C or Ctrl+D at any time to quit cleanly.
