from Board import Board

def display(board: Board) -> str:
    string_board = ''

    for row in board.board:
        for tile in row:   # check if the tile contain a treasure, if not contains, return the tail
            if tile.treasure:
                string_board += str(tile.treasure) + ' '
            elif tile.player:
                string_board += str(tile.player.name) + ' '
            else:
                string_board += str(tile.description) + ' '
        string_board += '\n'
    return string_board
