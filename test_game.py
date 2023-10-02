from Treasure import Treasure
from Board import Board

def test_treasure():
    t1 = Treasure(10)
    t2 = Treasure(20, description='%')

    assert t1.value == 10
    assert t1.description == '$'
    assert t2.value == 20
    assert t2.description == '$'

# def test_board():
#     with pytest.raises(ValueError, match='n must not be less than 2'):
#         b = Board(1, 5, 5, 10, 2)