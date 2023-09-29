from Treasure import Treasure
from Tile import Tile
import random

class Board:
    def __init__(self, n, t, min_val, max_val):
        # Handle Invalid Input
        # check if the value is match
        if not isinstance(n, int) or not isinstance(t, int) or not isinstance(min_val, int) or not isinstance(max_val, int):
            raise TypeError("Please enter int number.")
        if n <= 0 or t < 0 or min_val <= 0 or max_val <= 0 or min_val >= max_val or t > n * n:
            raise ValueError("Please enter valid argument values.")
        # Creates a square n x n collection board with Tile
        self.board = [[Tile() for _ in range(n)] for _ in range(n)]

        # Place treasures randomly
        for _ in range(t):
            while True:
                x = random.randint(0, n - 1)    # random coordinate
                y = random.randint(0, n - 1)
                # if there is no treasure, place the treasure in it
                if not self.board[y][x].treasure:
                    self.board[y][x].treasure = Treasure(random.randint(min_val, max_val))
                    break
