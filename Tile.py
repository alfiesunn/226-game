from Treasure import Treasure

class Tile:
    def __init__(self, description: str = '.', treasure: Treasure = None):
        self.description = description
        self.treasure = treasure
        self.player = None

    def __str__(self):
        if self.treasure:
            return self.treasure.description
        else:
            return self.treasure    # return default value

    def add_player(self, player):
        self.player = player    # add a player to the tile

