"""Automated tests for guess.py.

Run with:  python3 test_guess.py

No test framework needed - this uses only the standard library. The trick that
makes the game testable is in play() below: we replace random.randint so the
secret number is predictable, and replace input() so the "player" is a scripted
list of strings instead of a human typing.
"""

import contextlib
import importlib
import io
from unittest.mock import patch


def play(inputs, secret=42, interrupt=None):
    """Play one full game and return everything it printed.

    inputs    -- list of strings the fake player types, in order
    secret    -- the number the game will pick (normally random)
    interrupt -- 'eof' to simulate Ctrl+D, or 'ctrlc' to simulate Ctrl+C,
                 raised once the scripted inputs run out
    """
    guess = importlib.import_module("guess")
    remaining = list(inputs)

    def fake_input(prompt=""):
        if remaining:
            return remaining.pop(0)
        if interrupt == "eof":
            raise EOFError
        if interrupt == "ctrlc":
            raise KeyboardInterrupt
        raise AssertionError("the game asked for more input than the test supplied")

    captured = io.StringIO()
    with patch.object(guess.random, "randint", return_value=secret), \
            patch("builtins.input", fake_input), \
            contextlib.redirect_stdout(captured):
        guess.main()
    return captured.getvalue()


results = []


def check(name, passed):
    """Record one test result."""
    results.append((name, passed))


# --- Input that isn't a whole number should be rejected, not crash ---------
for label, bad_input in [
    ("superscript two", "²"),
    ("letters", "abc"),
    ("empty string", ""),
    ("a decimal", "3.5"),
    ("scientific notation", "1e3"),
    ("only spaces", "   "),
    ("an emoji", "\U0001f642"),
]:
    output = play([bad_input, "42"])
    check(
        f"rejects {label} and keeps playing",
        "Please enter a whole number." in output and "You got it!" in output,
    )

# --- Guesses outside 1-100 should be rejected -----------------------------
for label, bad_input in [
    ("zero", "0"),
    ("101", "101"),
    ("a negative number", "-5"),
    ("an enormous number", "99999999999999999999"),
]:
    output = play([bad_input, "42"])
    check(f"rejects {label}", "Please guess a number between 1 and 100." in output)

# --- The ends of the range are valid guesses ------------------------------
check("accepts the lowest guess (1)", "You got it!" in play(["1"], secret=1))
check("accepts the highest guess (100)", "You got it!" in play(["100"], secret=100))

# --- Attempts are counted correctly ---------------------------------------
check(
    "invalid and out-of-range guesses don't count as attempts",
    "It took you 1 attempt." in play(["abc", "999", "42"]),
)
check("a one-guess win reads '1 attempt'", "It took you 1 attempt." in play(["42"]))
check("a two-guess win reads '2 attempts'", "It took you 2 attempts." in play(["10", "42"]))

# --- Hints point the right way --------------------------------------------
output = play(["10", "90", "42"])
check("says 'Too low!' when the guess is below", "Too low!" in output)
check("says 'Too high!' when the guess is above", "Too high!" in output)

# --- Quitting exits cleanly instead of crashing ---------------------------
for label, how in [("Ctrl+D", "eof"), ("Ctrl+C", "ctrlc")]:
    output = play(["10"], interrupt=how)
    check(f"{label} says 'Thanks for playing!'", "Thanks for playing!" in output)
    check(f"{label} doesn't claim the player won", "You got it!" not in output)


# --- Report ---------------------------------------------------------------
passed_count = sum(1 for _, passed in results if passed)
for name, passed in results:
    print(f"{'PASS' if passed else 'FAIL'}  {name}")
print(f"\n{passed_count}/{len(results)} tests passed")

raise SystemExit(0 if passed_count == len(results) else 1)
