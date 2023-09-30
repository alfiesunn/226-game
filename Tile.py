from Treasure import Treasure

class Tile:
    def __init__(self, description: str = '.', treasure: Treasure = None):
        self.description = description
        self.treasure = treasure
        self.player = None

    def __str__(self):
        if self.treasure is not None:
            return self.treasure.description
        elif self.player is not None:
            return self.player.name
        else:
            return self.description    # return default value

    def add_player(self, player):
        self.player = player    # add a player to the tile

