import unittest

from app import App, ScrambleGenerator


class TestApp(unittest.TestCase):
    def test_scramble(self):
        self.moves = ["U", "U'", "U2", "D", "D'", "D2", "R", "R'",
                      "R2", "L", "L'", "L2", "F", "F'", "F2", "B", "B'", "B2"]
        scramble = ScrambleGenerator.generate_scramble(self)
        self.test_moves = scramble.split()
        self.assertEqual(len(self.test_moves), 20)

        for i in range(len(self.test_moves) - 1):
            assert self.test_moves[i] != self.test_moves[i +
                                                         1], f"Repeating move {self.test_moves[i]} at position {i}"

    def test_tutorial(self):
        app = App()
        self.test_images = app.images
        self.test_titles = app.titles
        self.assertEqual(len(self.test_titles), 25)
        self.assertEqual(len(self.test_images), 119)
        self.file = "solves.txt"
        with open(self.file) as f:
            self.file_count = sum(1 for line in f)
        self.listbox_count = app.listbox.size()
        self.assertEqual(self.file_count, self.listbox_count)
