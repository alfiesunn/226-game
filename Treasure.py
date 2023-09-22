class Treasure:
    def __init__(self, description='$', value=None):
        self.value = value
        self.description = description

    def __str__(self):
        return f'{self.description}{self.value}'
