class Treasure:
    def __init__(self, value=None, description='$'):
        if not isinstance(value, int) or value is None:
            raise ValueError("Value is required.")
        self.value = value
        self.description = description

    def __str__(self):
        return self.description