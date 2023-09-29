from Board import Board

def display(board: Board):
    for roll in board.board:
        for tile in roll:
            if tile.treasure:
                print(tile.treasure.description, end=" ")
            else:
                print(tile.description, end=" ")
        print()