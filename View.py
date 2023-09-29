from Board import Board

def display(board: Board):
    for row in board.board:
        for tile in row:
            if tile.treasure:   # check if the tile contain a treasure, if not contains, return the tail
                print(tile.treasure.description, end=" ")
            else:
                print(tile.description, end=" ")
        print()