import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from feedback import evaluate
from game import WordleGame


class FeedbackTests(unittest.TestCase):
    def test_duplicate_letters_are_consumed_once(self):
        self.assertEqual(evaluate("crane", "aaaaa"),
                         ["gray", "gray", "green", "gray", "gray"])
        self.assertEqual(evaluate("apple", "poppy"),
                         ["yellow", "gray", "green", "gray", "gray"])
        self.assertEqual(evaluate("banana", "aaaaaa"),
                         ["gray", "green", "gray", "green", "gray", "green"])

    def test_exact_absent_and_lengths(self):
        for word in ("game", "apple", "banana"):
            self.assertEqual(evaluate(word, word), ["green"] * len(word))
            self.assertEqual(evaluate(word, "z" * len(word)), ["gray"] * len(word))
        with self.assertRaises(ValueError):
            evaluate("game", "games")


class GameTests(unittest.TestCase):
    def play(self, length, target, inputs):
        game = WordleGame(length, target=target)
        output = io.StringIO()
        with patch("builtins.input", side_effect=inputs), redirect_stdout(output):
            outcome = game.run()
        return game, outcome, output.getvalue()

    def test_modes_and_invalid_guesses(self):
        for length, word in ((4, "game"), (5, "apple"), (6, "banana")):
            game, outcome, output = self.play(length, word, ["", "12", "x", word])
            self.assertEqual(outcome, "won")
            self.assertEqual(len(game.history), 1)
            self.assertIn("Session summary: won; 1 accepted guess(es).", output)
            self.assertEqual(output.count("  1. "), 2)

    def test_win_on_sixth_guess(self):
        game, outcome, output = self.play(4, "game", ["zzzz"] * 5 + ["game"])
        self.assertEqual(outcome, "won")
        self.assertEqual(len(game.history), 6)
        self.assertIn("Solved in 6 guess(es)!", output)

    def test_loss(self):
        game, outcome, output = self.play(5, "apple", ["zzzzz"] * 6)
        self.assertEqual(outcome, "lost")
        self.assertEqual(len(game.history), 6)
        self.assertIn("The word was apple", output)

    def test_quit(self):
        game, outcome, output = self.play(6, "banana", ["zzzzzz", "q"])
        self.assertEqual(outcome, "quit")
        self.assertEqual(len(game.history), 1)
        self.assertIn("Session summary: quit; 1 accepted guess(es).", output)


if __name__ == "__main__":
    unittest.main()
