from enum import Enum


class CharacterEmotion(Enum):
    NEUTRAL = 0
    SAD = 1
    ANGRY = 2

    def __str__(self):
        return self.name
