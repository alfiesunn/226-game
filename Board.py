from Treasure import Treasure
from Tile import Tile
from Player import Player
import random

class Board:
    def __init__(self, n, t, min_val, max_val, max_players):
        self.players = {}       # set a dictionaries for players
        self.n = n              # set board size
        self.max_players = max_players      # set maximum number of players

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
                x = random.randint(0, n - 1)    # random x-coordinate
                y = random.randint(0, n - 1)    # random y-coordinate
                # if there is no treasure, place the treasure in it
                if not self.board[y][x].treasure:
                    self.board[y][x].treasure = Treasure(random.randint(min_val, max_val))
                    break
        if not (0 <= max_players <= n):
                raise ValueError("Players number is out of range.")


    """ This is add player method to create a player"""
    def add_player(self, name, x, y):
        if x < 0 or y < 0 or len(self.players) > self.max_players:
            raise ValueError("Value is bigger than maximum.")
        if self.board[x][y].player:
            raise ValueError("Tile already there.")

        player = Player(name)                       # Create a new player object
        self.players[name] = {}                     # Initialize the player dictionary entry
        self.players[name]['location'] = (x, y)     # return player location
        self.players[name]['score'] = 0             # return player score

        self.board[x][y].add_player(player)         # Add the player to the board

    """ This is move a player method for a specified diection"""
    def move_player(self, name, direction):
        if name not in self.players:
            raise ValueError("Players not found")

        x, y = self.players[name]['location']       # Get the player's current location

        # Change the player's location
        match direction:
            case 'U':
                x -= 1
            case 'D':
                x += 1
            case  'L':
                y -= 1
            case  'R':
                y += 1
            case _:
                raise ValueError("Unknown command")

        print(self.players)

        if x < 0 or y < 0 or x >= len(self.board) or y >= len(self.board) or self.board[x][y].player:
             print("Move not allowed.")
        else:
            # Update player's position
            self.board[self.players[name]['location'][0]][self.players[name]['location'][1]].player = None
            self.players[name]['location'] = (x, y)     # setup the new location in the dictionary
            self.board[x][y].add_player(Player(name))


        # check the treasure if it is in the board
        if self.board[x][y].treasure is not None:
            score_increment = self.board[x][y].treasure.value
            print(self.players[name])
            self.players[name]['score'] += score_increment      # Update the player's score
            self.board[x][y].treasure = None        # Remove the treasure

    # Check if there are any treasures left on the board
    def count_treasures(self):
        for row in self.board:
            for tile in row:
                if tile.treasure:
                    return True     # Return True if a treasure is found
            return False