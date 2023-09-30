#!/usr/bin/python3.11
import random

from Board import Board
from View import display


board = Board(10, 5, 5, 10, 2)
board.add_player("1", random.randint(0, board.n - 1), random.randint(0, board.n - 1))
board.add_player("2", random.randint(0, board.n - 1), random.randint(0, board.n - 1))

# while board.count_treasures():
while True:
    display(board)


    playerInput = input('Which player do you want to move, 1 or 2\n')
    userInput = input('(U)p (L)eft (R)ight (D)own (Q)uit?\n ').upper()

    if userInput != 'Q':
        pass
    else:
        exit()

    board.move_player(playerInput, userInput)

    if not isinstance(userInput, str):
        raise TypeError("Error type.")

    for name, obj in board.players.items():
        # print(f"Player {name} the score is {board.players[name]['score']}")
        print(f"Player {name} the score is {obj['score']}")




