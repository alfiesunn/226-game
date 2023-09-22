from Treasure import Treasure

class Tile:
    def __init__(self, description='.', treasure: Treasure = None):
        self.description = description
        self.treasure = treasure

    def __str__(self):
        return f'{self.description}{self.treasure}'

