class Tile:
    def __init__(self):
        self.description = '.'
        self.treasure = None

    def __str__(self):
        return f'{self.description}{self.treasure}'

