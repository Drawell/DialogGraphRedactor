from enum import Enum
from gui.graphics_socket import QDMGraphicsSocket


class ESocketPosition(Enum):
    LEFT_TOP = 1
    LEFT_BOTTOM = 2
    RIGHT_TOP = 3
    RIGHT_BOTTOM = 4


class Socket:
    def __init__(self, node, index=0, position=ESocketPosition.LEFT_TOP):
        self.node = node
        self.index = index
        self.position = position
        self.gr_socket = QDMGraphicsSocket(self, self.node.gr_node)
        self.gr_socket.set_on_position(index, position in [ESocketPosition.LEFT_TOP, ESocketPosition.LEFT_BOTTOM],
                                       position in [ESocketPosition.LEFT_TOP, ESocketPosition.RIGHT_TOP])
