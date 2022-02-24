from enum import Enum
from typing import List


class Color(Enum):
    CADET_BLUE = 1
    CHARTREUSE = 2
    ORANGE = 3
    RED = 4
    YELLOW = 5

class Letter(Enum):
    A = 1
    B = 2
    C = 3
    D = 4
    E = 5
    F = 6
    G = 7
    H = 8

class Position(object):
    def __init__(self, column: Letter, row: int):
        self.column = column
        self.row = row
        self.hit = False

    def __eq__(self, other):
        return self.column == other.column and self.row == other.row

    def __str__(self):
        return f"{self.column.name}{self.row}"

    __repr__ = __str__

class Ship(object):
    def __init__(self, name: str, size: int, color: Color):
        self.name = name
        self.size = size
        self.color = color
        self.positions: List[Position] = []
        self.is_sunk = False

    def shoot(self, input: Position):
        for position in self.positions:
            if input.__eq__(position):
                position.hit = True
        self.check_if_sunk()

    def check_if_sunk(self):
        temp = True
        for position in self.positions:
            temp &= position.hit
        self.is_sunk = temp

    def add_position(self, input: Position):
        self.positions.append(input)

    def __str__(self):
        return f"{self.color.name} {self.name} ({self.size}): {self.positions}"

    __repr__ = __str__
