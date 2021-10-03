from enum import Enum


class CharacterEmotion(Enum):
    NEUTRAL = 0
    SAD = 1
    ANGRY = 2
    HAPPY = 3
    FRIGHTENED = 4
    SURPRISED = 5

    def __str__(self):
        return self.name
