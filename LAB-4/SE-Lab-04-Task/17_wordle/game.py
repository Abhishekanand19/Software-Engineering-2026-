import random
from words import WORDS
from feedback import evaluate


class WordleGame:
    MAX_GUESSES = 6

    def __init__(self, length=5, target=None):
        choices = [word for word in WORDS if len(word) == length]
        if not choices:
            raise ValueError(f"No words available with {length} letters.")
        self.length = length
        self.target = target if target is not None else random.choice(choices)
        if self.target not in choices:
            raise ValueError("Target must be a word in the selected mode.")
        self.history = []

    def run(self):
        print(f"Wordle - {self.length} letters, {self.MAX_GUESSES} guesses. Type q to quit.")
        while len(self.history) < self.MAX_GUESSES:
            try:
                guess = input("> ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                guess = "q"
            if guess == "q":
                print("Game quit.")
                self.show_summary("quit")
                return "quit"
            if len(guess) != self.length or not guess.isascii() or not guess.isalpha():
                print(f"Enter a {self.length}-letter word.")
                continue
            feedback = evaluate(self.target, guess)
            self.history.append((guess, feedback))
            self.show_history()
            if guess == self.target:
                print(f"Solved in {len(self.history)} guess(es)!")
                self.show_summary("won")
                return "won"
        print(f"Out of guesses. The word was {self.target}.")
        self.show_summary("lost")
        return "lost"

    def show_history(self):
        print("History:")
        for number, (guess, colors) in enumerate(self.history, 1):
            print(f"  {number}. {guess.upper()}  {' '.join(colors)}")

    def show_summary(self, outcome):
        print(f"Session summary: {outcome}; {len(self.history)} accepted guess(es).")
        if self.history:
            self.show_history()
