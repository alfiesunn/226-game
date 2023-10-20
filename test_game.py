from Treasure import Treasure
from Tile import Tile
from Player import Player
from Board import Board
import pytest

# test treasure
def test_treasure():
    t1 = Treasure(10)
    t2 = Treasure(20, description='$')

    assert t1.value == 10
    assert t1.description == '$'
    assert t2.value == 20
    assert t2.description == '$'

# test tile
def test_tile():
    tile1 = Tile()
    tile2 = Tile(description='.',treasure=None)

    assert tile1.treasure == None
    assert tile1.description == '.'
    assert tile2.treasure == None
    assert tile2.description == '.'

# test player
def test_player():
    player1 = Player('Seer')
    player2 = Player('Gakuto')

    assert player1.name == 'Seer'
    assert player1.score == 0
    assert player2.name == 'Gakuto'
    assert player2.score == 0

# test board
def test_board_type():
    with pytest.raises(TypeError, match='Please enter int number.'):
        b = Board(1.5, 5.5, 5.5, 10.5, 2)

# test the available value
def test_board_value():
    with pytest.raises(ValueError, match='Please enter valid argument values.'):
        b = Board(-1,5,5,10,2)

# test the player number out of range
def test_play_number():
    with pytest.raises(ValueError, match='Players number is out of range.'):
        b = Board(10,5,5,10,11)

# test add player in the board
def test_add_play():
    with pytest.raises(ValueError, match='Value is bigger than maximum.'):
        b = Board(10,5,5,10,2)
        b.add_player('Seer', -1,2)

# test check the both player exist in the same location or not
def test_player_exist():
    with pytest.raises(ValueError, match='Player already there.'):
        b = Board(10,5,5,10,2)
        b.add_player('Seer', 1, 2)
        b.add_player('Seer', 1, 2)

# test the player in the list or not
def test_move_play():
    with pytest.raises(ValueError, match='Players not found'):
        b = Board(10, 5, 5, 10, 2)
        b.add_player('Seer', 1,2)
        b.move_player('Se', 'U')

# test the player valid direction
def test_player_direction():
    with pytest.raises(ValueError, match='Unknown command'):
        b = Board(10,5,5,10,2)
        b.add_player('Seer', 2,2)
        b.move_player('Seer','W')

# test the player valid movement, out of the board or not
def test_player_move():
    with pytest.raises(ValueError, match='Move not allowed.'):
        b = Board(10,5,5,10,2)
        # x is row, y is columns
        b.add_player('Seer', 9,0)
        b.move_player('Seer','D')

# test the player can move into another player location
def test_move_into_player():
    with pytest.raises(ValueError, match='Move not allowed.'):
        b = Board(10, 5, 5, 10, 2)
        b.add_player('Seer', 1, 2)
        b.add_player('Gakuto', 1, 3)
        b.move_player('Seer','R')

# test if player collects a treasure
def test_player_collects_treasure():
        b = Board(10,5,5,10,2)
        score_increment = 10
        b.board[1][3].treasure = Treasure(score_increment)
        b.add_player('Seer', 1,2)
        b.move_player('Seer', 'R')
        assert b.players['Seer']['score'] == score_increment





