class Player:
    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError("You need to type a string.")
        self.name = name
        self.score = 0

    def add_score(self, scores):
        self.score += scores

    def total_score(self):
        return self.score

