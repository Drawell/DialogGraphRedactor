from enum import Enum


class CharacterPosition(Enum):
    LEFT_BOTTOM = 0
    RIGHT_BOTTOM = 1
    LEFT_TOP = 2
    RIGHT_TOP = 3
    CENTER = 4

    def __str__(self):
        return self.name