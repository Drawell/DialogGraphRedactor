from enum import Enum


class SocketType(Enum):
    INPUT = 1
    OUTPUT = 2

    def __str__(self):
        return self.name
