"""Project 3 - Number guessing game.

A game built from loops, conditionals and functions. The logic is separate from
input/output so it can be tested: `play` takes a function that supplies guesses.

Run:
    python 03_number_guessing_game.py          # play interactively
    python 03_number_guessing_game.py --demo   # scripted, deterministic game
Standard library only.
"""
import random
import sys


def judge(guess, secret):
    if guess < secret:
        return "too low"
    if guess > secret:
        return "too high"
    return "correct"


def play(secret, get_guess, max_tries=7, output=print):
    """Play one game. get_guess() returns the next guess as text. Returns tries used, or None if lost."""
    for attempt in range(1, max_tries + 1):
        raw = get_guess()
        try:
            guess = int(raw)
        except ValueError:
            output(f"attempt {attempt}: '{raw}' is not a whole number")
            continue
        verdict = judge(guess, secret)
        output(f"attempt {attempt}: {guess} is {verdict}")
        if verdict == "correct":
            return attempt
    output(f"out of tries; the number was {secret}")
    return None


def run_demo():
    rng = random.Random(42)          # fixed seed makes the secret reproducible
    secret = rng.randint(1, 100)
    scripted = iter(["50", "abc", "75", "90", "82"])
    tries = play(secret, lambda: next(scripted))
    print("result:", "won in " + str(tries) + " tries" if tries else "lost")


def main(argv):
    if "--demo" in argv:
        run_demo()
        return 0
    secret = random.randint(1, 100)
    print("I am thinking of a number from 1 to 100. You have 7 tries.")
    tries = play(secret, lambda: input("Your guess: "))
    print("You won!" if tries else "Better luck next time.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
