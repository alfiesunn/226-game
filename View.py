from Board import Board

def display(board: Board):
    for row in board.board:
        for tile in row:   # check if the tile contain a treasure, if not contains, return the tail
            print(tile, end=" ")
            # else:
            #     print(tile.description, end=" ")
        print()