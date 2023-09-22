#!/usr/bin/python3.11

class Treasure:
    def __init__(self):
        self.value = None
        self.description = '$'

    def __str__(self):
        return f'{self.description}{self.value}'
